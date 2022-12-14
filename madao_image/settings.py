"""Settings file for madao image."""
from pydantic import BaseSettings


class Settings(BaseSettings):
    """Base Settings."""

    PROJECT_NAME: str = "Madao Image"

    PROJECT_DESCRIPTION: str = "A image processing service."

    PROJECT_VERSION: str = "0.1.0"

    DOCS_URL: str = "/docs"

    REDOC_URL: str = "/redoc"

    OPENAPI_URL: str = "/openapi.json"

    ALLOWED_HOSTS: list[str] = ["*"]

    CORS_ORIGINS: list[str] = ["*"]

    CORS_ALLOW_METHODS: list[str] = ["*"]

    CORS_ALLOW_HEADERS: list[str] = ["*"]

    CORS_ALLOW_CREDENTIALS: bool = True

    DEBUG: bool = False

    class Config:
        """Override the default config."""

        env_file = ".env"


settings = Settings()
