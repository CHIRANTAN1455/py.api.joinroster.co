from functools import lru_cache
from pathlib import Path
import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings


PROJECT_ROOT = Path(__file__).resolve().parents[2]
LOCAL_ENV_PATH = PROJECT_ROOT / ".env"
LARAVEL_ROOT = PROJECT_ROOT.parent / "api.joinroster.co"
LARAVEL_ENV_PATH = LARAVEL_ROOT / ".env"


def load_laravel_env() -> None:
    """
    Load env: Laravel .env first (base), then local .env in FastAPI project
    overrides. So you can put a .env in the project root with your values.
    """
    if LARAVEL_ENV_PATH.exists():
        load_dotenv(dotenv_path=LARAVEL_ENV_PATH, override=False)
    if LOCAL_ENV_PATH.exists():
        load_dotenv(dotenv_path=LOCAL_ENV_PATH, override=True)


load_laravel_env()


class Settings(BaseSettings):
    """
    Central application settings.

    All Laravel .env keys are exposed via `os.environ` unchanged; this
    Settings object is mainly for FastAPI-specific configuration.
    """

    APP_NAME: str = "py.api.joinroster.co"
    APP_ENV: str = os.getenv("APP_ENV", "local")
    APP_DEBUG: bool = os.getenv("APP_DEBUG", "false").lower() == "true"

    # Database (use Laravel-style variables directly)
    DB_CONNECTION: str = os.getenv("DB_CONNECTION", "mysql")
    DB_HOST: str = os.getenv("DB_HOST", "127.0.0.1")
    DB_PORT: int = int(os.getenv("DB_PORT", "3306"))
    DB_DATABASE: str = os.getenv("DB_DATABASE", "")
    DB_USERNAME: str = os.getenv("DB_USERNAME", "")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")

    # JWT configuration (mapping from Laravel Sanctum / app key)
    JWT_SECRET: str = os.getenv("JWT_SECRET") or os.getenv("APP_KEY", "change-me")
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRES_IN_SECONDS: int = 60 * 60 * 24

    # Redis / queues / cache / mail / third-parties are accessed directly
    # from os.environ using their Laravel names (e.g. STRIPE_SECRET).

    class Config:
        env_prefix = ""  # keep names identical to Laravel .env
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()

