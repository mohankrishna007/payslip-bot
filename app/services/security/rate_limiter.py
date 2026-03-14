from dataclasses import dataclass, field
from datetime import date

from app.config import settings


@dataclass
class _Bucket:
    count: int = 0
    day: date = field(default_factory=date.today)


class RateLimiter:
    """Per-user daily request counter.

    Counts are kept in memory; the counter resets automatically when
    the calendar day changes.
    """

    def __init__(self) -> None:
        self._store: dict[str, _Bucket] = {}

    def check_and_increment(self, user_id: str) -> bool:
        """Return True and increment the counter if the user is within the daily limit.

        Returns False (blocked) if they have reached MAX_REQUESTS_PER_DAY today.
        """
        today = date.today()
        bucket = self._store.get(user_id)

        if bucket is None or bucket.day != today:
            self._store[user_id] = _Bucket(count=1, day=today)
            return True

        if bucket.count >= settings.max_requests_per_day:
            return False

        bucket.count += 1
        return True


# Module-level singleton and backward-compatible alias.
_rate_limiter = RateLimiter()
check_and_increment = _rate_limiter.check_and_increment
