import base64

import ollama

from app.config import settings
from app.providers.base import LLMProvider


class OllamaProvider(LLMProvider):
    def __init__(self) -> None:
        self._client = ollama.Client(host=settings.ollama_base_url)

    async def analyze_image(self, image_bytes: bytes, prompt: str) -> str:
        b64 = base64.b64encode(image_bytes).decode()
        resp = self._client.generate(
            model=settings.ollama_model,
            prompt=prompt,
            images=[b64],
        )
        return resp["response"]
