from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    database_url: str
    es_url: str
    huggingface_api_key: str
    gemini_api_key: str
    secret_key: str


settings = Settings()  # type: ignore
