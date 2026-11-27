from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "development"
    database_url: str = ""
    supabase_url: str = ""
    supabase_anon_key: str = ""
    admin_user_ids: str = ""
    cors_origins: str = "http://localhost:5173"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def admin_ids(self) -> set[str]:
        return {value.strip() for value in self.admin_user_ids.split(",") if value.strip()}

    @property
    def cors_origin_list(self) -> list[str]:
        values = [value.strip() for value in self.cors_origins.split(",") if value.strip()]
        return values or ["http://localhost:5173"]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
