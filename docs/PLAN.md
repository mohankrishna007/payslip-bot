# Plan: SalaryBot Local Build (No WhatsApp)

## Context
- PRD: SalaryBot_PRD_v1.md
- Interface: FastAPI Swagger UI + REST (no WhatsApp Business API)
- LLM local default: LLaVA 1.5 7B via Ollama (needs 8GB RAM, no API key, ~4GB download once)
- LLM mock: mock_provider for CI/CD or when Ollama is not running
- LLM prod: Gemini Flash (primary) + GPT-4o Mini (fallback) via env vars
- DB: SQLite (local); Supabase is a 1-file swap for prod
- Rate limiting: in-memory dict (no Redis needed locally)
- Provider priority: ollama → mock → gemini → openai

## Project Structure
```
payslip-bot/
├── app/
│   ├── main.py                  # FastAPI app, all routes
│   ├── config.py                # pydantic-settings, loads from .env
│   ├── schemas.py               # Pydantic request/response models
│   ├── providers/
│   │   ├── __init__.py          # get_provider() factory
│   │   ├── base.py              # LLMProvider ABC
│   │   ├── ollama_provider.py   # LLaVA 1.5 7B via Ollama (local default)
│   │   ├── mock_provider.py     # Canned response, no dependency
│   │   ├── gemini.py            # Gemini Flash (prod primary)
│   │   └── openai_provider.py   # GPT-4o Mini (prod fallback)
│   ├── services/
│   │   ├── file_handler.py      # PDF/image → clean JPEG, EXIF strip
│   │   ├── pii_scrubber.py      # Post-LLM response PII removal
│   │   ├── formatter.py         # Emoji map + EN/HI output + viral footer
│   │   ├── rate_limiter.py      # In-memory rate limiter (10/day/user)
│   │   ├── session_store.py     # In-memory chat context (24h TTL)
│   │   └── deduction_checker.py # F7: statutory rules engine (PF/ESI/PT)
│   └── db/
│       └── database.py          # SQLite via aiosqlite
├── tests/
│   ├── test_pii_scrubber.py
│   ├── test_file_handler.py
│   ├── test_deduction_checker.py
│   └── sample_slips/            # 2-3 test images/PDFs
├── .env.example
├── requirements.txt
└── README.md
```

## Phases

### Phase 1: Project Foundation
- requirements.txt:
  fastapi, uvicorn[standard], python-multipart, pillow, pymupdf,
  pydantic-settings, python-dotenv, google-generativeai, openai,
  ollama, aiosqlite, httpx, pytest, pytest-asyncio, anyio
- .env.example keys:
  LLM_PROVIDER=ollama
  OLLAMA_BASE_URL=http://localhost:11434
  OLLAMA_MODEL=llava:7b
  GEMINI_API_KEY=
  OPENAI_API_KEY=
  SQLITE_PATH=./salarybot.db
  MAX_REQUESTS_PER_DAY=10
- app/config.py: pydantic-settings Settings class
- app/main.py: FastAPI app + GET /health → {"status": "ok", "provider": "ollama"}
- README.md: prerequisite — install Ollama, then `ollama pull llava:7b`

### Phase 2: LLM Provider Abstraction Layer (PAL)
- app/providers/base.py: LLMProvider ABC
    async def analyze_image(self, image_bytes: bytes, prompt: str) -> str
- app/providers/ollama_provider.py (LOCAL DEFAULT):
    import ollama, base64
    client = ollama.Client(host=settings.OLLAMA_BASE_URL)
    b64 = base64.b64encode(image_bytes).decode()
    resp = client.generate(model=settings.OLLAMA_MODEL, prompt=prompt, images=[b64])
    return resp['response']
- app/providers/mock_provider.py: returns hardcoded realistic salary breakdown string
- app/providers/gemini.py: google.generativeai vision call (prod primary)
- app/providers/openai_provider.py: base64 image + openai chat completions (prod fallback)
- app/providers/__init__.py: get_provider(name: str) -> LLMProvider factory

### Phase 3: File Processing Pipeline (parallel with Phase 2)
- app/services/file_handler.py:
    detect_file_type(data: bytes) -> Literal["image", "pdf"]
    pdf_to_image(data: bytes) -> bytes          # PyMuPDF, page 1 only, returns JPEG
    normalize_image(data: bytes) -> bytes       # Pillow: converts PNG/WebP → JPEG
    strip_exif(data: bytes) -> bytes            # Pillow: removes GPS/device metadata
    validate_image_size(data: bytes, max_mb=5)  # raises HTTPException if too large

### Phase 4: PII Scrubbing — 3 layers (parallel with Phase 3)
- Layer 1 — SALARY_PROMPT instruction: "Do NOT include employee name, PAN number, or bank account number in your response"
- Layer 2 — app/services/pii_scrubber.py: scrub(text: str) -> str
    PAN regex: r'[A-Z]{5}[0-9]{4}[A-Z]' → [REDACTED]
    Account: r'\b\d{9,18}\b' → [REDACTED]
    Applied to LLM response before returning to user
- Layer 3 — same scrub() applied to text stored in session_store before saving

### Phase 5: Core Analysis Engine (depends on Phase 2+4)
- SALARY_PROMPT constant (in app/services/prompts.py):
    Instructs LLM to extract all salary components, explain each in plain language,
    note what is deductible vs. what is employer benefit, respond in {language}
- app/services/formatter.py:
    EMOJI_MAP: dict of component name → emoji prefix
    format_response(raw: str, language: str) -> str
    Appends viral footer: "Found this helpful? Forward to a colleague 👇"

### Phase 6: Rate Limiting + SQLite DB
- app/services/rate_limiter.py:
    In-memory dict[user_id → {count: int, date: date}], max=MAX_REQUESTS_PER_DAY
    check_and_increment(user_id: str) -> bool (False = blocked)
- app/db/database.py: aiosqlite
    Table: users (id, session_id TEXT UNIQUE, consent_given BOOL, created_at)
    Table: slip_events (id, user_id, processed_at, provider_used, language)
    init_db() called on app startup

### Phase 6.5: Session Store for Chat (parallel with Phase 6)
- app/services/session_store.py:
    In-memory: dict[user_id → {analysis: str, expires_at: datetime}]
    set_session(user_id, analysis_text)  # overwrites on new /analyze
    get_session(user_id) -> str | None   # returns None if expired (>24h)
    PII-scrubbed before storage

### Phase 7: Deduction Checker — F7 (parallel with Phase 6)
- app/services/deduction_checker.py:
    check(components: dict) -> list[{field, expected, actual, status: "ok"|"flag"}]
    Rules:
      PF employee = 12% of Basic (±5% tolerance; mandatory if basic > ₹15,000)
      ESI = 0.75% of gross (only applicable if gross < ₹21,000)
      PT = ₹200/month for Maharashtra (if salary > ₹10,000); configurable per state
    Components dict is extracted from LLM response via simple key:value parsing

### Phase 8: API Endpoints (depends on Phase 3–7)
- POST /consent          body: {user_id: str} → records consent in SQLite
- POST /analyze          multipart: file + form fields {user_id, language}
                         pipeline: validate → detect type → normalize → strip EXIF →
                         rate check → LLM (with PII exclusion in prompt) →
                         pii_scrubber on response → format + viral footer →
                         store in session_store → log event → return explanation
- POST /chat             body: {user_id: str, message: str}
                         retrieves session context → sends context+message to LLM → scrub → return
- POST /check            body: {user_id: str}
                         retrieves session context → runs deduction_checker → returns flags
- GET  /history/{user_id} → last 10 slip_events for user (metadata only)
- GET  /health           → {"status": "ok", "provider": LLM_PROVIDER}
- app/schemas.py: Pydantic models for all request/response shapes

### Phase 9: Tests
- tests/test_pii_scrubber.py: PAN match, account match, clean text passthrough, no false positives on rupee amounts
- tests/test_file_handler.py: PDF→JPEG, PNG→JPEG, EXIF stripped, oversized file rejected
- tests/test_deduction_checker.py: PF correct, ESI flagged when gross > ₹21k, PT wrong amount flagged
- tests/sample_slips/: 2-3 sample salary slip images/PDFs for manual Swagger testing
- Integration smoke: POST /consent → POST /analyze (mock provider) → POST /chat → POST /check

## Decisions
- user_id is a free-form string (simulates WhatsApp phone number; no auth in local dev)
- LLM_PROVIDER=ollama is the default; set to mock for pure pipeline tests with no Ollama
- PII scrubber runs on LLM *response text*, not image pixels (vision model, can't regex pixels)
- Session store is in-memory; resets on server restart (acceptable for local dev)
- Rate limiter is in-memory; resets on restart (acceptable for local dev)
- Multi-page PDF: only page 1 processed (per PRD decision)
- PNG/WebP inputs normalized to JPEG before LLM call (Ollama and all providers accept JPEG)
- LLaVA quality is lower than Gemini Flash — acceptable for pipeline validation, not for prod
- Language auto-detect deferred; explicit "en"/"hi" field in request for local dev
