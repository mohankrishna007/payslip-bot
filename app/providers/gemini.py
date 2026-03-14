import logging

from google import genai
from google.genai import errors, types
from tenacity import retry, retry_if_exception, stop_after_attempt, wait_exponential

from app.config import settings
from app.providers.base import LLMProvider

log = logging.getLogger("salarybot")


def _is_gemini_rate_limit(exc: Exception) -> bool:
    return isinstance(exc, errors.ClientError) and exc.code == 429


class GeminiProvider(LLMProvider):
    def __init__(self) -> None:
        self._client = genai.Client(
            api_key=settings.gemini_api_key,
            http_options={"api_version": "v1beta"},
        )

    async def analyze_image(self, image_bytes: bytes, prompt: str) -> str:
        image_part = types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg")
        return await self._call(image_part, prompt)

    async def chat(self, prompt: str) -> str:
        return await self._call_text(prompt)

    # ── Internal retry-wrapped helpers ────────────────────────────────────────

    _retry = dict(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=60, min=60, max=300),
        retry=retry_if_exception(_is_gemini_rate_limit),
        before_sleep=lambda rs: log.warning(
            "Gemini rate limited, retrying in %.0fs (attempt %s/3)",
            rs.next_action.sleep,
            rs.attempt_number,
        ),
        reraise=True,
    )

    @retry(**_retry)
    async def _call(self, image_part: types.Part, prompt: str) -> str:
        response = await self._client.aio.models.generate_content(
            model=settings.gemini_model,
            contents=[prompt, image_part],
        )
        return response.text

    @retry(**_retry)
    async def _call_text(self, prompt: str) -> str:
        response = await self._client.aio.models.generate_content(
            model=settings.gemini_model,
            contents=[prompt],
        )
        return response.text
