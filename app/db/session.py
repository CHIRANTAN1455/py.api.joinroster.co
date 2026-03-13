from urllib.parse import quote_plus

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.core.config import get_settings


def _build_database_url() -> str:
    """
    Build a SQLAlchemy connection URL from Laravel-style DB_* settings.
    Defaults to MySQL-compatible URL since the original app is Laravel.
    Username and password are URL-encoded so special chars (@, :, etc.) work.
    """
    settings = get_settings()
    user = quote_plus(settings.DB_USERNAME)
    password = quote_plus(settings.DB_PASSWORD)

    if settings.DB_CONNECTION == "mysql":
        return (
            f"mysql+pymysql://{user}:{password}"
            f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_DATABASE}"
        )

    if settings.DB_CONNECTION == "pgsql":
        return (
            f"postgresql+psycopg2://{user}:{password}"
            f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_DATABASE}"
        )

    # Fallback: let SQLAlchemy try the raw DB_CONNECTION as a URL
    return settings.DB_CONNECTION


DATABASE_URL = _build_database_url()

# Timeouts for remote DBs; pool_recycle avoids stale connections
_connect_args = {
    "connect_timeout": 30,
    "read_timeout": 60,
    "write_timeout": 60,
}
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    connect_args=_connect_args,
    pool_recycle=280,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

