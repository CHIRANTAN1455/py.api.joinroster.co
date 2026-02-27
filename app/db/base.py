from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy ORM models."""

    pass


# Import models here so that Alembic / metadata discovery can find them.
# from app.db.models.user import User  # noqa: F401
# from app.db.models.project import Project  # noqa: F401

