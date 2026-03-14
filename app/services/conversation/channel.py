"""Channel abstraction — Template Method pattern.

Each delivery channel (WhatsApp, in-app web) is a subclass of Channel.

  Channel (ABC)
  ├── on_text(user_id, text)    → str   # invariant algorithm
  └── on_upload(user_id, data)  → str   # invariant algorithm
      ↑  subclasses supply the three channel-specific strings:
      greeting / file_request / needs_file

The algorithm (state machine, LLM calls, PII scrubbing, session management)
lives here once.  To change internal processing, edit this file — both channels
are automatically affected.  To change how a reply is worded for a specific
channel, edit the concrete subclass below.
"""

import logging
from abc import ABC, abstractmethod

from app.config import settings
from app.db.database import record_consent
from app.providers import get_provider
from app.services.conversation.messages import (
    CONSENT_PROMPT,
    DECLINE,
    FILE_TOO_LARGE,
    NO_WORDS,
    PARSE_ERROR,
    RATE_LIMIT,
    RESET_WORDS,
    SESSION_EXPIRED,
    YES_WORDS,
)
from app.services.conversation.state import State, get_state, reset, set_state
from app.services.payslip.prompts import CHAT_FOLLOW_UP_PROMPT
from app.services.payslip.service import (
    FileTooLargeError,
    ParseFailedError,
    RateLimitedError,
    process_payslip,
)
from app.services.security.pii_scrubber import scrub
from app.services.session.store import get_session

log = logging.getLogger("salarybot.channel")


# ── Abstract base ──────────────────────────────────────────────────────────────

class Channel(ABC):
    """Abstract channel.

    Defines the conversation algorithm (Template Method).
    Concrete subclasses supply channel-specific message strings.
    """

    # ── Channel-specific strings (override in each subclass) ──────────────

    @property
    @abstractmethod
    def greeting(self) -> str:
        """Consent-request greeting sent on first contact."""

    @property
    @abstractmethod
    def file_request(self) -> str:
        """Message asking the user to upload their payslip after consent."""

    @property
    @abstractmethod
    def needs_file(self) -> str:
        """Message sent when the user texts instead of uploading."""

    # ── Template methods (invariant algorithm — do NOT override) ──────────

    async def on_text(self, user_id: str, text: str) -> str:
        """Advance the state machine for a text message; return the reply.

        Flow (same for every channel):
          INIT             → send greeting, move to AWAITING_CONSENT
          AWAITING_CONSENT → handle yes/no, move to AWAITING_FILE or reset
          AWAITING_FILE    → remind user to upload
          CHAT             → answer follow-up via LLM
        """
        lower = text.lower().strip()
        state = get_state(user_id)

        if lower in RESET_WORDS:
            reset(user_id)
            state = State.INIT

        if state == State.INIT:
            set_state(user_id, State.AWAITING_CONSENT)
            return self.greeting

        if state == State.AWAITING_CONSENT:
            if lower in YES_WORDS:
                await record_consent(user_id)
                set_state(user_id, State.AWAITING_FILE)
                return self.file_request
            if lower in NO_WORDS:
                reset(user_id)
                return DECLINE
            return CONSENT_PROMPT

        if state == State.AWAITING_FILE:
            return self.needs_file

        # ── CHAT: answer follow-up questions ──────────────────────────────
        context = get_session(user_id)
        if context is None:
            reset(user_id)
            set_state(user_id, State.AWAITING_CONSENT)
            return SESSION_EXPIRED + self.greeting

        provider = get_provider(settings.llm_provider)
        raw = await provider.chat(
            CHAT_FOLLOW_UP_PROMPT.format(context=context, question=text)
        )
        return scrub(raw)

    async def on_upload(self, user_id: str, data: bytes) -> str:
        """Process a payslip upload; return the reply.

        Pass data=b"" when the state gate will reject the upload before the
        bytes are needed (INIT / AWAITING_CONSENT) to avoid unnecessary
        media downloads (WhatsApp channel does this).
        """
        state = get_state(user_id)

        if state == State.INIT:
            set_state(user_id, State.AWAITING_CONSENT)
            return self.greeting

        if state == State.AWAITING_CONSENT:
            return CONSENT_PROMPT

        try:
            result = await process_payslip(user_id, data)
            return result.formatted
        except FileTooLargeError:
            return FILE_TOO_LARGE
        except RateLimitedError:
            return RATE_LIMIT
        except ParseFailedError:
            return PARSE_ERROR


# ── Concrete channels ──────────────────────────────────────────────────────────

class WhatsAppChannel(Channel):
    """WhatsApp delivery channel.

    Uses WhatsApp-native markdown: *bold*, _italic_, bullet lists with •.
    """

    @property
    def greeting(self) -> str:
        return (
            "👋 Hey! I'm *SalaryBuddy* — your friendly payslip assistant.\n\n"
            "I help Indian employees understand their salary slips in simple everyday language.\n\n"
            "Before we start, I need your permission to process your payslip.\n"
            "🔒 _I only analyse your payslip and never store personal details like your name, PAN, or bank account._\n\n"
            "Do you agree? Reply *YES* to continue or *NO* to cancel."
        )

    @property
    def file_request(self) -> str:
        return (
            "✅ Let's go!\n\n"
            "📎 Please send me your payslip as:\n"
            "• A *photo* (JPEG or PNG)\n"
            "• A *PDF* document\n\n"
            "_I'll analyse it and explain everything in plain language._"
        )

    @property
    def needs_file(self) -> str:
        return "Please send your payslip as a photo or PDF so I can help. 📎"


class WebChannel(Channel):
    """In-app web delivery channel.

    Plain text — the browser UI (Renderer.js) handles all markdown rendering.
    Wording uses "upload" instead of "send" since the user interacts via a
    file picker, not a WhatsApp attachment.
    """

    @property
    def greeting(self) -> str:
        return (
            "👋 Hi! I'm *SalaryBuddy*.\n\n"
            "I'll break down your payslip in plain English — no jargon, no confusion.\n\n"
            "🔒 Your data stays private. I never store your name, PAN, or bank details.\n\n"
            "Ready to start? Reply *YES* to continue."
        )

    @property
    def file_request(self) -> str:
        return (
            "Great! 📎 Upload your payslip to get started.\n\n"
            "Accepted formats: JPEG, PNG, or PDF."
        )

    @property
    def needs_file(self) -> str:
        return "Go ahead and upload your payslip — I'm ready when you are. 📎"
