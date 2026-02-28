"""Shortlist: user shortlists project or creator."""
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from app.db.base import Base


class Shortlist(Base):
    __tablename__ = "shortlists"
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(36), unique=True, index=True, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
