import logging
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import JSONResponse

from app.config import settings

# ---------------------------------------------------------------------------
# Logging setup — structured, timestamped, visible in terminal
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger("salarybot")
from app.db.database import get_history, init_db, log_slip_event, record_consent
from app.providers import get_provider
from app.schemas import (
    AnalyzeResponse,
    ChatRequest,
    ChatResponse,
    CheckRequest,
    CheckResponse,
    ConsentRequest,
    ConsentResponse,
    DeductionResult,
    HealthResponse,
    HistoryResponse,
    SlipEvent,
)
from app.services.deduction_checker import check as check_deductions
from app.services.file_handler import (
    compress_for_llm,
    detect_file_type,
    normalize_image,
    pdf_to_image,
    strip_exif,
    validate_image_size,
)
from app.services.json_parser import extract_json
from app.services.pii_scrubber import scrub
from app.services.prompts import SALARY_PROMPT
from app.services.rate_limiter import check_and_increment
from app.services.session_store import get_session, set_session


@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info("Starting SalaryBot — provider=%s  db=%s", settings.llm_provider, settings.sqlite_path)
    await init_db()
    log.info("Database initialised")
    yield
    log.info("SalaryBot shutting down")


app = FastAPI(title="SalaryBot", version="1.0.0", lifespan=lifespan)


# ---------------------------------------------------------------------------
# Request / response logging middleware
# ---------------------------------------------------------------------------

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.perf_counter()
    log.info("→ %s %s", request.method, request.url.path)
    try:
        response = await call_next(request)
    except Exception as exc:
        log.exception("Unhandled error during %s %s", request.method, request.url.path)
        raise
    elapsed_ms = (time.perf_counter() - start) * 1000
    log.info("← %s %s  status=%d  %.0fms", request.method, request.url.path, response.status_code, elapsed_ms)
    return response


# ---------------------------------------------------------------------------
# GET /health
# ---------------------------------------------------------------------------

@app.get("/health", response_model=HealthResponse)
async def health():
    log.debug("Health check")
    return {"status": "ok", "provider": settings.llm_provider}


# ---------------------------------------------------------------------------
# POST /consent
# ---------------------------------------------------------------------------

@app.post("/consent", response_model=ConsentResponse)
async def consent(body: ConsentRequest):
    log.info("Consent recorded  user=%s", body.user_id)
    await record_consent(body.user_id)
    return {"detail": "Consent recorded."}


# ---------------------------------------------------------------------------
# POST /analyze
# ---------------------------------------------------------------------------

@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze(
    file: UploadFile = File(...),
    user_id: str = Form(...),
    language: str = Form("en"),
):
    data = await file.read()
    log.info("Analyze request  user=%s  lang=%s  filename=%s  size=%d bytes", user_id, language, file.filename, len(data))

    # 1. Size guard
    validate_image_size(data)

    # 2. Convert PDF → JPEG if needed
    file_type = detect_file_type(data)
    log.info("Detected file type: %s", file_type)
    if file_type == "pdf":
        data = pdf_to_image(data)
        log.info("PDF converted to JPEG  size=%d bytes", len(data))

    # 3. Normalise to JPEG + strip EXIF + compress for LLM
    data = normalize_image(data)
    data = strip_exif(data)
    data = compress_for_llm(data)
    log.info("Image normalised, EXIF stripped, compressed  final_size=%d bytes", len(data))

    # 4. Rate limit
    if not check_and_increment(user_id):
        log.warning("Rate limit exceeded  user=%s", user_id)
        raise HTTPException(
            status_code=429,
            detail=f"Daily limit of {settings.max_requests_per_day} requests reached. Try again tomorrow.",
        )

    # 5. Build prompt and call LLM
    prompt = SALARY_PROMPT
    log.info("Calling LLM provider=%s", settings.llm_provider)
    provider = get_provider(settings.llm_provider)
    raw = await provider.analyze_image(data, prompt)
    log.info("LLM response received  chars=%d", len(raw))

    # 6. PII scrub LLM response
    scrubbed = scrub(raw)

    # 7. Parse JSON from LLM output (handles wrapping/stringification)
    try:
        parsed = extract_json(scrubbed)
    except ValueError as exc:
        log.error("JSON extraction failed: %s", exc)
        raise HTTPException(status_code=502, detail="LLM returned an unreadable response. Please try again.")

    # 8. Persist raw JSON string in session store for chat context
    set_session(user_id, scrubbed)
    log.info("Session stored  user=%s", user_id)

    # 9. Log event to DB
    await log_slip_event(user_id, settings.llm_provider, language)

    return {"data": parsed}


# ---------------------------------------------------------------------------
# POST /chat
# ---------------------------------------------------------------------------

@app.post("/chat", response_model=ChatResponse)
async def chat(body: ChatRequest):
    log.info("Chat request  user=%s  message_len=%d", body.user_id, len(body.message))
    context = get_session(body.user_id)
    if context is None:
        log.warning("No session found for chat  user=%s", body.user_id)
        raise HTTPException(
            status_code=404,
            detail="No active session found. Please upload a salary slip first via /analyze.",
        )

    prompt = (
        f"Context — previous salary slip analysis:\n{context}\n\n"
        f"User question: {body.message}\n\n"
        "Answer concisely based on the context above."
    )

    provider = get_provider(settings.llm_provider)
    raw = await provider.analyze_image(b"", prompt)
    reply = scrub(raw)
    log.info("Chat reply sent  user=%s  reply_len=%d", body.user_id, len(reply))
    return {"reply": reply}


# ---------------------------------------------------------------------------
# POST /check
# ---------------------------------------------------------------------------

@app.post("/check", response_model=CheckResponse)
async def check(body: CheckRequest):
    log.info("Check request  user=%s", body.user_id)
    context = get_session(body.user_id)
    if context is None:
        log.warning("No session found for check  user=%s", body.user_id)
        raise HTTPException(
            status_code=404,
            detail="No active session found. Please upload a salary slip first via /analyze.",
        )

    # Extract key:value pairs from the stored analysis text
    components: dict[str, str] = {}
    for match in re.finditer(r"([A-Za-z ]+):\s*₹?([\d,]+)", context):
        key = match.group(1).strip().lower()
        components[key] = match.group(2).replace(",", "")

    log.info("Extracted %d components for deduction check", len(components))
    results = check_deductions(components)
    flagged = sum(1 for r in results if r["status"] == "flag")
    log.info("Deduction check complete  total=%d  flagged=%d  user=%s", len(results), flagged, body.user_id)
    return {"results": [DeductionResult(**r) for r in results]}


# ---------------------------------------------------------------------------
# GET /history/{user_id}
# ---------------------------------------------------------------------------

@app.get("/history/{user_id}", response_model=HistoryResponse)
async def history(user_id: str):
    log.info("History request  user=%s", user_id)
    events = await get_history(user_id)
    log.info("Returning %d events  user=%s", len(events), user_id)
    return {"events": [SlipEvent(**e) for e in events]}
