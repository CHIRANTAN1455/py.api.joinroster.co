from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import relationship

from app.db.base import Base


class Project(Base):
    """
    SQLAlchemy representation of Laravel's `Project` model.

    The table name matches exactly (`projects`) and includes a subset of
    important fields from the migration spec. Additional attributes can be
    added as needed while preserving compatibility.
    """

    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(36), unique=True, index=True, nullable=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    editor_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    title = Column(String(255), nullable=False)
    custom_title = Column(String(255), nullable=True)
    description = Column(Text, nullable=False)
    budget = Column(Numeric(12, 2), nullable=True)
    budget_per = Column(String(50), nullable=True)

    status = Column(String(50), nullable=True)
    flow = Column(String(50), nullable=True)
    match_token = Column(String(255), nullable=True)

    utc_offset = Column(String(10), nullable=True)
    timezone = Column(String(100), nullable=True)
    city = Column(String(255), nullable=True)
    country = Column(String(255), nullable=True)

    published = Column(Integer, default=0)

    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    deleted_at = Column(DateTime, nullable=True)

    user = relationship("User", foreign_keys=[user_id], back_populates="projects")

