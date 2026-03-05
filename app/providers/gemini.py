import asyncio
import logging

from google import genai
from google.genai import errors, types

from app.config import settings
from app.providers.base import LLMProvider

log = logging.getLogger("salarybot")

_RETRIES = 3


class GeminiProvider(LLMProvider):
    def __init__(self) -> None:
        self._client = genai.Client(
            api_key=settings.gemini_api_key,
            http_options={"api_version": "v1beta"},
        )

    async def analyze_image(self, image_bytes: bytes, prompt: str) -> str:
        image_part = types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg")
        for attempt in range(_RETRIES):
            try:
                response = await self._client.aio.models.generate_content(
                    model=settings.gemini_model,
                    contents=[prompt, image_part],
                )
                return response.text
            except errors.ClientError as exc:
                if exc.code == 429 and attempt < _RETRIES - 1:
                    wait = (2 ** attempt) * 60  # 5s, 10s, 20s
                    log.warning("Gemini rate limited, retrying in %ss (attempt %s/%s)", wait, attempt + 1, _RETRIES)
                    await asyncio.sleep(wait)
                else:
                    raise
        raise RuntimeError("Gemini: all retries exhausted")
