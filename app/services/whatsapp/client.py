"""WhatsApp Business Cloud API client.

Handles:
  • Sending text messages
  • Downloading media (image / PDF) by media_id
"""

import logging

import httpx

from app.config import settings

log = logging.getLogger("salarybot.whatsapp")

_GRAPH_BASE = "https://graph.facebook.com"


async def send_text(to: str, text: str) -> None:
    """Send a plain-text WhatsApp message to *to* (E.164 phone number)."""
    url = f"{_GRAPH_BASE}/{settings.wa_api_version}/{settings.wa_phone_number_id}/messages"
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text, "preview_url": False},
    }
    await _post(url, payload)


async def download_media(media_id: str) -> bytes:
    """Fetch media bytes for a given WhatsApp *media_id*.

    Step 1 — resolve the temporary download URL from the Graph API.
    Step 2 — download the raw bytes using the same bearer token.
    """
    headers = {"Authorization": f"Bearer {settings.wa_access_token}"}

    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.get(
            f"{_GRAPH_BASE}/{settings.wa_api_version}/{media_id}",
            headers=headers,
        )
        r.raise_for_status()
        media_url: str = r.json()["url"]

    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.get(media_url, headers=headers)
        r.raise_for_status()
        return r.content


async def _post(url: str, payload: dict) -> None:
    headers = {
        "Authorization": f"Bearer {settings.wa_access_token}",
        "Content-Type": "application/json",
    }
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(url, json=payload, headers=headers)
        if r.status_code >= 400:
            log.error(
                "WhatsApp API error  status=%d  body=%s",
                r.status_code,
                r.text[:500],
            )
            r.raise_for_status()
