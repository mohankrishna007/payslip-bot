"""WhatsApp Cloud API webhook — protocol adapter for WhatsAppChannel.

This file is intentionally thin: it handles only WhatsApp-specific plumbing
(webhook verification, Meta message envelope parsing, media download, send_text
delivery).  All conversation logic lives in WhatsAppChannel (channel.py).

Conversation flow (handled inside WhatsAppChannel.on_text / on_upload):
  INIT             -> greeting + AWAITING_CONSENT
  AWAITING_CONSENT -> yes/no handling + AWAITING_FILE or reset
  AWAITING_FILE    -> remind to upload
  CHAT             -> LLM follow-up Q&A
"""

import logging

from fastapi import APIRouter, Query, Request
from fastapi.exceptions import HTTPException
from fastapi.responses import PlainTextResponse

from app.config import settings
from app.services.conversation.channel import WhatsAppChannel
from app.services.conversation.messages import GENERIC_ERROR
from app.services.conversation.state import State, get_state
from app.services.whatsapp.client import download_media, send_text

router = APIRouter()
log = logging.getLogger("salarybot.webhook")

_channel = WhatsAppChannel()

# WhatsApp-only UX strings (not part of the state machine)
_PROCESSING   = "⏳ Got it! Analysing your payslip — give me a moment..."
_UNKNOWN_FILE = (
    "I can only read *images* (JPEG, PNG) or *PDF* documents. "
    "Please send your payslip in one of those formats. 📎"
)


# ---------------------------------------------------------------------------
# GET /webhook - Meta verification handshake
# ---------------------------------------------------------------------------

@router.get("/webhook")
async def verify_webhook(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_verify_token: str = Query(None, alias="hub.verify_token"),
    hub_challenge: str = Query(None, alias="hub.challenge"),
):
    if hub_mode == "subscribe" and hub_verify_token == settings.wa_verify_token:
        log.info("WhatsApp webhook verified successfully")
        return PlainTextResponse(hub_challenge)
    log.warning("WhatsApp webhook verification failed  mode=%s", hub_mode)
    raise HTTPException(status_code=403, detail="Webhook verification failed")


# ---------------------------------------------------------------------------
# POST /webhook - incoming messages from WhatsApp
# ---------------------------------------------------------------------------

@router.post("/webhook")
async def receive_webhook(request: Request):
    body = await request.json()
    for entry in body.get("entry", []):
        for change in entry.get("changes", []):
            for msg in change.get("value", {}).get("messages", []):
                await _dispatch(msg)
    return {"status": "ok"}  # always 200 - Meta will retry on non-2xx


# ---------------------------------------------------------------------------
# Internal dispatch
# ---------------------------------------------------------------------------

async def _dispatch(msg: dict) -> None:
    user_id: str | None = msg.get("from")
    msg_type: str = msg.get("type", "")
    if not user_id:
        return

    log.info("Message  from=%s  type=%s", user_id, msg_type)
    try:
        if msg_type == "text":
            text = msg.get("text", {}).get("body", "").strip()
            reply = await _channel.on_text(user_id, text)
            await send_text(user_id, reply)

        elif msg_type in ("image", "document"):
            await _handle_media(user_id, msg, msg_type)

        else:
            await send_text(
                user_id,
                "I can only process text messages and payslip images or PDFs. 😊",
            )
    except Exception:
        log.exception("Unhandled error  user=%s", user_id)
        await send_text(user_id, GENERIC_ERROR)


async def _handle_media(user_id: str, msg: dict, msg_type: str) -> None:
    # Guard: send greeting / consent prompt without downloading media
    if get_state(user_id) in (State.INIT, State.AWAITING_CONSENT):
        reply = await _channel.on_upload(user_id, b"")
        await send_text(user_id, reply)
        return

    media_id: str | None = msg.get(msg_type, {}).get("id")
    if not media_id:
        await send_text(user_id, _UNKNOWN_FILE)
        return

    await send_text(user_id, _PROCESSING)
    data = await download_media(media_id)
    reply = await _channel.on_upload(user_id, data)
    await send_text(user_id, reply)