from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    llm_provider: str = "gemini"
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.0-flash-lite"
    openai_api_key: str = ""
    openai_model: str = "gpt-5-nano"
    sqlite_path: str = "./salarybot.db"
    max_requests_per_day: int = 10

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
