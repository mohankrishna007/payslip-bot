from abc import ABC, abstractmethod


class LLMProvider(ABC):
    @abstractmethod
    async def analyze_image(self, image_bytes: bytes, prompt: str) -> str:
        """Analyse a salary slip image and return a plain-text explanation."""
