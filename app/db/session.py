from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.core.config import get_settings


def _build_database_url() -> str:
    """
    Build a SQLAlchemy connection URL from Laravel-style DB_* settings.
    Defaults to MySQL-compatible URL since the original app is Laravel.
    """
    settings = get_settings()

    if settings.DB_CONNECTION == "mysql":
        return (
            f"mysql+pymysql://{settings.DB_USERNAME}:{settings.DB_PASSWORD}"
            f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_DATABASE}"
        )

    if settings.DB_CONNECTION == "pgsql":
        return (
            f"postgresql+psycopg2://{settings.DB_USERNAME}:{settings.DB_PASSWORD}"
            f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_DATABASE}"
        )

    # Fallback: let SQLAlchemy try the raw DB_CONNECTION as a URL
    return settings.DB_CONNECTION


DATABASE_URL = _build_database_url()

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

