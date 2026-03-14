"""Per-user conversation state machine."""

from enum import Enum

# In-memory store: user_id → State  (reset on server restart)
_state: dict[str, str] = {}


class State(str, Enum):
    INIT = "INIT"
    AWAITING_CONSENT = "AWAITING_CONSENT"
    AWAITING_FILE = "AWAITING_FILE"
    CHAT = "CHAT"


def get_state(user_id: str) -> State:
    return State(_state.get(user_id, State.INIT))


def set_state(user_id: str, state: State) -> None:
    _state[user_id] = state.value


def reset(user_id: str) -> None:
    """Clear the user's conversation state (e.g. on restart/reset command)."""
    _state.pop(user_id, None)
