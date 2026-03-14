import base64

from openai import AsyncOpenAI

from app.config import settings
from app.providers.base import LLMProvider


class OpenAIProvider(LLMProvider):
    def __init__(self) -> None:
        self._client = AsyncOpenAI(api_key=settings.openai_api_key)

    async def analyze_image(self, image_bytes: bytes, prompt: str) -> str:
        b64 = base64.b64encode(image_bytes).decode()
        response = await self._client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{b64}"},
                        },
                    ],
                }
            ],
        )
        return response.choices[0].message.content

    async def chat(self, prompt: str) -> str:
        response = await self._client.chat.completions.create(
            model=settings.openai_model,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content
