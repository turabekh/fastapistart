import os
from typing import List

from pydantic import PostgresDsn, RedisDsn, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    APP_NAME: str = "MyFastAPIApp"
    DEBUG: bool = False

    # Server settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Database settings
    DATABASE_URL: PostgresDsn

    # Redis settings (if needed)
    REDIS_URL: RedisDsn | None = None

    # API settings
    API_VERSION: str = "/api/v1"
    ROOT_PATH: str = "/api/v1"

    # Security settings
    SECRET_KEY: SecretStr
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    model_config = SettingsConfigDict(
        case_sensitive=True,
    )


# Create a settings instance
settings = Settings()
