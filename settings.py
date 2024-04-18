from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import final


@final
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=('.env',),
        env_file_encoding='utf-8')

    debug: bool = True
    redis_url: str
    bot_token: str
    base_webhook_url: str
    webhook_path: str
    telegram_my_token: str

    tts_url: str
    stt_url: str
    api_token: str

    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: str


@lru_cache()  # get it from memory
def get_settings() -> Settings:
    return Settings()
