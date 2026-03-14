from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    llm_provider: str = "gemini"
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.0-flash-lite"
    openai_api_key: str = ""
    openai_model: str = "gpt-5-nano"
    sqlite_path: str = "./salarybot.db"
    max_requests_per_day: int = 10

    # WhatsApp Business Cloud API
    wa_phone_number_id: str = ""       # From Meta Developer Console
    wa_access_token: str = ""          # Permanent or temporary system user token
    wa_verify_token: str = ""              # Any secret string you choose
    wa_api_version: str = "v19.0"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
