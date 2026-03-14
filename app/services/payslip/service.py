"""Core payslip processing pipeline shared by all channels (WhatsApp, REST API, in-app chat).

Raises typed exceptions so callers can respond in their own channel-appropriate way —
HTTP errors for the REST router, friendly strings for the WhatsApp/in-app routers.
"""

import logging

from app.config import settings
from app.db.database import log_slip_event
from app.providers import get_provider
from app.services.conversation.state import State, set_state
from app.services.payslip.file_handler import compress_for_llm, detect_file_type, extract_pdf_text, normalize_image, pdf_to_image
from app.services.payslip.json_parser import extract_json
from app.services.payslip.formatter import format_analysis
from app.services.payslip.prompts import SALARY_PROMPT, SALARY_TEXT_PROMPT
from app.services.security.pii_scrubber import scrub
from app.services.security.rate_limiter import check_and_increment
from app.services.session.store import set_session

log = logging.getLogger("salarybot.payslip_service")

_MAX_FILE_MB = 5.0


# ── Typed exceptions ───────────────────────────────────────────────────────────

class FileTooLargeError(Exception):
    """Raised when the uploaded file exceeds the maximum allowed size."""


class RateLimitedError(Exception):
    """Raised when the user has exceeded their daily request quota."""


class ParseFailedError(Exception):
    """Raised when the LLM response cannot be parsed as valid JSON."""


# ── Processing result ──────────────────────────────────────────────────────────

class PayslipResult:
    """Holds both the raw scrubbed text and the parsed JSON after successful analysis."""

    def __init__(self, scrubbed_text: str, parsed: dict) -> None:
        self.scrubbed_text = scrubbed_text
        self.parsed = parsed
        self.formatted = format_analysis(parsed)


# ── Pipeline ───────────────────────────────────────────────────────────────────

async def process_payslip(user_id: str, data: bytes, language: str = "en") -> PayslipResult:
    """Run the full payslip analysis pipeline for *user_id*.

    Steps: validate → convert PDF → normalise image → compress → rate-limit
           → call LLM → scrub PII → parse JSON → store session → log event.

    Returns a :class:`PayslipResult` on success.
    Raises :exc:`FileTooLargeError`, :exc:`RateLimitedError`, or
    :exc:`ParseFailedError` on recoverable failures.
    """
    if len(data) / (1024 * 1024) > _MAX_FILE_MB:
        raise FileTooLargeError

    # ── Determine input modality ───────────────────────────────────────────
    pdf_text: str | None = None
    file_type = detect_file_type(data)

    if file_type == "pdf":
        pdf_text = extract_pdf_text(data)          # None → scanned/image PDF
        if pdf_text is None:
            # Scanned PDF — fall back to image pipeline
            data = pdf_to_image(data)
            data = normalize_image(data)
            data = compress_for_llm(data)
    else:
        data = normalize_image(data)
        data = compress_for_llm(data)

    if not check_and_increment(user_id):
        raise RateLimitedError

    provider = get_provider(settings.llm_provider)
    if pdf_text is not None:
        log.info(
            "Calling LLM with extracted PDF text  provider=%s  user=%s  chars=%d",
            settings.llm_provider, user_id, len(pdf_text),
        )
        raw = await provider.chat(SALARY_TEXT_PROMPT.replace("__PAYSLIP_TEXT__", pdf_text))
    else:
        log.info("Calling LLM with image  provider=%s  user=%s", settings.llm_provider, user_id)
        raw = await provider.analyze_image(data, SALARY_PROMPT)
    scrubbed = scrub(raw)
    log.info("LLM response received  chars=%d  user=%s", len(scrubbed), user_id)

    try:
        parsed = extract_json(scrubbed)
    except ValueError as exc:
        log.error("JSON extraction failed for user=%s: %s", user_id, exc)
        raise ParseFailedError from exc

    set_session(user_id, scrubbed)
    set_state(user_id, State.CHAT)
    await log_slip_event(user_id, settings.llm_provider, language)

    return PayslipResult(scrubbed_text=scrubbed, parsed=parsed)
