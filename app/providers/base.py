from abc import ABC, abstractmethod


class LLMProvider(ABC):
    @abstractmethod
    async def analyze_image(self, image_bytes: bytes, prompt: str) -> str:
        """Analyse a salary slip image and return a plain-text explanation."""

    @abstractmethod
    async def chat(self, prompt: str) -> str:
        """Answer a text-only prompt (no image) and return a plain-text reply.

        Used for follow-up Q&A after the payslip has already been analysed.
        Separating this from analyze_image makes the intent explicit and avoids
        passing empty bytes to a vision model.
        """
