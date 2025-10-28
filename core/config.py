from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    mongodb_url: str
    database_name: str
    secret_key: str
    algorithm: str = "HS256"
    access_token_expiry: int = 30
    min_password_length: int = 8
    environment: str = "development"

    model_config = SettingsConfigDict(env_file=".env", extra="allow")


@lru_cache
def get_settings() -> Settings:
    return Settings()
