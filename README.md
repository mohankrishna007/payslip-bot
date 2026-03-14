# SalaryBuddy

AI-powered payslip explainer — FastAPI backend with Gemini / OpenAI vision models.

## Prerequisites

### 1. Python environment

Requires Python 3.10+.

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

### 2. Configuration

Copy `.env.example` to `.env` and fill in your keys:

```bash
cp .env.example .env   # macOS / Linux
copy .env.example .env  # Windows
```

| Variable | Default | Description |
|---|---|---|
| `LLM_PROVIDER` | `gemini` | Active provider: `gemini` \| `openai` |
| `GEMINI_API_KEY` | _(required for gemini)_ | Google AI Studio API key |
| `GEMINI_MODEL` | `gemini-2.0-flash-lite` | Gemini model name |
| `OPENAI_API_KEY` | _(required for openai)_ | OpenAI API key |
| `OPENAI_MODEL` | `gpt-5-nano` | OpenAI model name |
| `SQLITE_PATH` | `./salarybot.db` | SQLite database file path |
| `MAX_REQUESTS_PER_DAY` | `10` | Per-user daily rate limit |
| `WA_PHONE_NUMBER_ID` | _(optional)_ | Meta WhatsApp phone number ID |
| `WA_ACCESS_TOKEN` | _(optional)_ | Meta WhatsApp access token |
| `WA_VERIFY_TOKEN` | _(optional)_ | Webhook verification secret |
| `WA_API_VERSION` | `v19.0` | Meta Graph API version |

WhatsApp variables are only needed when using the `/webhook` endpoints. Leave them blank to run in web-chat-only mode.

## Running the server

```bash
uvicorn app.main:app --reload
```

Open **http://localhost:8000** for the chat UI, or **/docs** for the API explorer.

## Health check

```
GET /health
→ {"status": "ok", "provider": "gemini"}
```

