# SalaryBot

AI-powered salary slip explainer — FastAPI backend with LLaVA vision model.

## Prerequisites

### 1. Install Ollama

Download and install Ollama from https://ollama.com/download, then pull the default model:

```bash
ollama pull llava:7b
```

This downloads ~4 GB once. Ollama must be running before starting the server.

### 2. Python environment

Requires Python 3.10+.

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

### 3. Configuration

Copy `.env.example` to `.env` and fill in any optional keys:

```bash
cp .env.example .env
```

| Variable | Default | Description |
|---|---|---|
| `LLM_PROVIDER` | `ollama` | Active provider: `ollama` \| `mock` \| `gemini` \| `openai` |
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama server URL |
| `OLLAMA_MODEL` | `llava:7b` | Ollama vision model tag |
| `GEMINI_API_KEY` | _(empty)_ | Required when `LLM_PROVIDER=gemini` |
| `OPENAI_API_KEY` | _(empty)_ | Required when `LLM_PROVIDER=openai` |
| `SQLITE_PATH` | `./salarybot.db` | SQLite database file path |
| `MAX_REQUESTS_PER_DAY` | `10` | Per-user daily rate limit |

Set `LLM_PROVIDER=mock` to run the full pipeline without Ollama (useful for CI/CD or quick tests).

## Running the server

```bash
uvicorn app.main:app --reload
```

Open the interactive API docs at http://localhost:8000/docs.

## Health check

```
GET /health
→ {"status": "ok", "provider": "ollama"}
```
