from datetime import datetime, timedelta

from app.services.pii_scrubber import scrub

_TTL_HOURS = 24

# user_id → {analysis: str, expires_at: datetime}
_store: dict[str, dict] = {}


def set_session(user_id: str, analysis_text: str) -> None:
    """Store a PII-scrubbed analysis for the user, overwriting any previous entry."""
    _store[user_id] = {
        "analysis": scrub(analysis_text),
        "expires_at": datetime.utcnow() + timedelta(hours=_TTL_HOURS),
    }


def get_session(user_id: str) -> str | None:
    """Return the stored analysis, or None if not found or expired (>24 h)."""
    entry = _store.get(user_id)
    if entry is None:
        return None
    if datetime.utcnow() > entry["expires_at"]:
        del _store[user_id]
        return None
    return entry["analysis"]
