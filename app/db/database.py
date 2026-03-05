import aiosqlite

from app.config import settings

_CREATE_USERS = """
CREATE TABLE IF NOT EXISTS users (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id  TEXT    UNIQUE NOT NULL,
    consent_given BOOLEAN NOT NULL DEFAULT 0,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

_CREATE_SLIP_EVENTS = """
CREATE TABLE IF NOT EXISTS slip_events (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id      TEXT    NOT NULL,
    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    provider_used TEXT NOT NULL,
    language     TEXT NOT NULL
);
"""


async def init_db() -> None:
    """Create tables if they do not exist. Called once on app startup."""
    async with aiosqlite.connect(settings.sqlite_path) as db:
        await db.execute(_CREATE_USERS)
        await db.execute(_CREATE_SLIP_EVENTS)
        await db.commit()


async def record_consent(session_id: str) -> None:
    async with aiosqlite.connect(settings.sqlite_path) as db:
        await db.execute(
            "INSERT INTO users (session_id, consent_given) VALUES (?, 1) "
            "ON CONFLICT(session_id) DO UPDATE SET consent_given = 1",
            (session_id,),
        )
        await db.commit()


async def log_slip_event(user_id: str, provider_used: str, language: str) -> None:
    async with aiosqlite.connect(settings.sqlite_path) as db:
        await db.execute(
            "INSERT INTO slip_events (user_id, provider_used, language) VALUES (?, ?, ?)",
            (user_id, provider_used, language),
        )
        await db.commit()


async def get_history(user_id: str, limit: int = 10) -> list[dict]:
    async with aiosqlite.connect(settings.sqlite_path) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT id, user_id, processed_at, provider_used, language "
            "FROM slip_events WHERE user_id = ? ORDER BY processed_at DESC LIMIT ?",
            (user_id, limit),
        ) as cursor:
            rows = await cursor.fetchall()
    return [dict(row) for row in rows]
