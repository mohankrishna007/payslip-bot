from app.providers.base import LLMProvider


def get_provider(name: str) -> LLMProvider:
    """Return the LLMProvider instance for the given provider name."""
    name = name.lower()

    if name == "gemini":
        from app.providers.gemini import GeminiProvider
        return GeminiProvider()

    if name == "openai":
        from app.providers.openai_provider import OpenAIProvider
        return OpenAIProvider()

    raise ValueError(
        f"Unknown LLM provider '{name}'. Valid values: gemini, openai"
    )
