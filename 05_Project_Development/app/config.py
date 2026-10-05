import os
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")


class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "PocketSmart AI")
    APP_ENV: str = os.getenv("APP_ENV", "development")

    SECRET_KEY: str = os.getenv(
        "SECRET_KEY",
        "development-only-change-this-secret",
    )

    DATABASE_PATH: str = os.getenv(
        "DATABASE_PATH",
        str(PROJECT_ROOT / "pocketsmart.db"),
    )

    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "").strip()
    GEMINI_MODEL: str = os.getenv(
        "GEMINI_MODEL",
        "gemini-2.5-flash",
    )

    SESSION_HTTPS_ONLY: bool = (
        os.getenv("SESSION_HTTPS_ONLY", "false").lower() == "true"
    )

    MAX_UPLOAD_MB: int = int(os.getenv("MAX_UPLOAD_MB", "5"))


settings = Settings()