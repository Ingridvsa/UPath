# app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, AliasChoices
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "UPath API"
    API_V1_PREFIX: str = "/api/v1"
    CORS_ORIGINS: List[str] = ["*"]

    # aceita tanto DATABASE_URL quanto DB_URL
    DATABASE_URL: str = Field(validation_alias=AliasChoices("DATABASE_URL", "DB_URL"))

    # JWT / Auth
    # SECRET_KEY do .env vai preencher JWT_SECRET
    JWT_SECRET: str = Field(
        "troque-isto-por-um-segredo-longo-e-aleatorio",
        alias="SECRET_KEY",
    )
    JWT_ALG: str = "HS256"

    # valor padrão, mas também é lido de ACCESS_TOKEN_EXPIRE_MINUTES do .env
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 30  # 30 dias

    APP_NAME: str = "uPath API"
    APP_ENV: str = "dev"

    ADMIN_PIN: str = Field("1234", alias="ADMIN_PIN")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

settings = Settings()
