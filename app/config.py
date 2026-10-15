"""Configuration module for SaferPassForge.

Loads and validates application settings from environment variables using
Pydantic Settings according to Twelve-Factor App and DRY principles.
"""

from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Centralized application configuration schema with strict typing and validation."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    APP_NAME: str = Field(
        default="SaferPassForge",
        description="Name of the application service.",
    )
    APP_ENV: Literal["development", "testing", "production"] = Field(
        default="development",
        description="Current runtime environment.",
    )
    APP_SECRET_KEY: str = Field(
        ...,
        min_length=16,
        description="Cryptographic secret key used for session/hashing security.",
    )
    DATABASE_URL: str = Field(
        default="sqlite:///./saferpassforge.db",
        description="Database connection string (SQLite for MVP).",
    )
    DEFAULT_PASSWORD_LENGTH: int = Field(
        default=16,
        ge=8,
        le=128,
        description="Default length for generated secure passwords.",
    )

    @property
    def is_production(self) -> bool:
        """Helper property to identify production environment."""
        return self.APP_ENV == "production"


@lru_cache
def get_settings() -> Settings:
    """Provides a cached instance of validated application settings.

    Returns:
        Settings: Validated settings loaded from .env and environment variables.
    """
    return Settings()

