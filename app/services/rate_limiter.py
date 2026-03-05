from dataclasses import dataclass, field
from datetime import date

from app.config import settings


@dataclass
class _Bucket:
    count: int = 0
    day: date = field(default_factory=date.today)


# user_id → _Bucket
_store: dict[str, _Bucket] = {}


def check_and_increment(user_id: str) -> bool:
    """Return True and increment counter if the user is within the daily limit.

    Returns False (blocked) if they have reached MAX_REQUESTS_PER_DAY today.
    Counter resets automatically when the calendar day changes.
    """
    today = date.today()
    bucket = _store.get(user_id)

    if bucket is None or bucket.day != today:
        _store[user_id] = _Bucket(count=1, day=today)
        return True

    if bucket.count >= settings.max_requests_per_day:
        return False

    bucket.count += 1
    return True
