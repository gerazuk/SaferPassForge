"""Tests for application settings and environment loading."""

from app.config import Settings, get_settings


def test_settings_load_from_env() -> None:
    """Verifies that Settings loads and validates default configuration values."""
    settings = get_settings()

    assert settings.APP_NAME == "SaferPassForge"
    assert settings.APP_ENV in ("development", "testing", "production")
    assert len(settings.APP_SECRET_KEY) >= 16
    assert "sqlite" in settings.DATABASE_URL
    assert 8 <= settings.DEFAULT_PASSWORD_LENGTH <= 128


def test_settings_is_production_flag() -> None:
    """Verifies the is_production helper property."""
    dev_settings = Settings(APP_SECRET_KEY="test-secret-key-with-sufficient-length", APP_ENV="development")
    assert not dev_settings.is_production

    prod_settings = Settings(APP_SECRET_KEY="test-secret-key-with-sufficient-length", APP_ENV="production")
    assert prod_settings.is_production

