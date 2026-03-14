import logging
import time
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.config import settings
from app.db.database import init_db
from app.api import webapp, webhook

# ---------------------------------------------------------------------------
# Logging setup — structured, timestamped, visible in terminal
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger("salarybot")


@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info("Starting SalaryBot — provider=%s  db=%s", settings.llm_provider, settings.sqlite_path)
    await init_db()
    log.info("Database initialised")
    yield
    log.info("SalaryBot shutting down")


app = FastAPI(title="SalaryBot", version="1.0.0", lifespan=lifespan)
app.mount("/static", StaticFiles(directory=Path(__file__).parent / "static"), name="static")

app.include_router(webhook.router)
app.include_router(webapp.router)

_ui = Jinja2Templates(directory=Path(__file__).parent / "templates")


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def index(request: Request):
    return _ui.TemplateResponse("chat.html", {"request": request})


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


