"""Shared bot message strings used by both the WhatsApp webhook and in-app chat routers.

Channel-specific phrasing (e.g. WhatsApp _italic_ / *bold* formatting,
or "send" vs "upload") lives in each router; only strings that are identical
across channels belong here.
"""

# ── Canned replies ─────────────────────────────────────────────────────────────

DECLINE         = "No worries! Come back anytime. 👋"
CONSENT_PROMPT  = "Just reply *YES* to continue or *NO* to cancel."
RATE_LIMIT      = "You've hit today's limit. Come back tomorrow and I'll be ready! 🙏"
FILE_TOO_LARGE  = "That file is too large (max 5 MB). Try a smaller or clearer photo."
PARSE_ERROR     = "Couldn't read that one clearly. Try a sharper image or a different PDF page."
GENERIC_ERROR   = "Something went wrong. Please try again in a moment."
SESSION_EXPIRED = "Your session expired — let's start fresh!\n\n"

# ── Consent word sets (shared state-machine logic) ─────────────────────────────

YES_WORDS   = frozenset({"yes", "y", "agree", "ok", "okay", "sure", "yep", "yeah", "haan", "ha"})
NO_WORDS    = frozenset({"no", "n", "nope", "cancel", "nahi", "na"})
RESET_WORDS = frozenset({"reset", "restart", "start over"})
