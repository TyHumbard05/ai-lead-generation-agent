from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    brave_search_api_key: str | None = None
    brave_search_url: str = "https://api.search.brave.com/res/v1/web/search"
    brave_country: str = "US"
    brave_search_lang: str = "en"
    http_timeout_seconds: float = 15.0

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
