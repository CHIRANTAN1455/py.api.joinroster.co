"""Matching: project–editor match. Laravel matchings or similar."""
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from app.db.base import Base


class Matching(Base):
    __tablename__ = "matchings"
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(36), unique=True, index=True, nullable=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    editor_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    token = Column(String(255), nullable=True)
    status = Column(String(50), nullable=True)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
