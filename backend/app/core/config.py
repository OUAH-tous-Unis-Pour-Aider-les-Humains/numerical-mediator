from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "numerical-mediator-api"
    api_host: str = "127.0.0.1"
    api_port: int = 8000
    log_level: str = "INFO"

    database_url: str = "postgresql+psycopg://mediator:mediator@localhost:5432/numerical_mediator"

    celery_broker_url: str = "redis://localhost:6379/0"
    celery_result_backend: str = "redis://localhost:6379/1"


@lru_cache
def get_settings() -> Settings:
    return Settings()
