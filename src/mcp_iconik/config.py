"""Configuration settings from environment variables."""

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    """Server configuration loaded from environment variables."""

    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    ICONIK_URL: str = os.getenv("ICONIK_URL", "https://app.iconik.io")
    ICONIK_API: str | None = os.getenv("ICONIK_API")
    ICONIK_APP_ID: str | None = os.getenv("ICONIK_APP_ID")
    ICONIK_AUTH_TOKEN: str | None = os.getenv("ICONIK_AUTH_TOKEN")
    DEBUG: bool = os.getenv("DEBUG", "").lower() == "true"


settings = Settings()
