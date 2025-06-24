from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    database_url: str
    hf_token: str
    gemini_api_key: str
    secret_key: str
    qdrant_url: str
    qdrant_api_key: str
    es_url: str
    redis_url: str


settings = Settings()  # type: ignore
