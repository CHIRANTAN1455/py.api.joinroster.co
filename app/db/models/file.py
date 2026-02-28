"""Uploaded file record."""
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from app.db.base import Base


class File(Base):
    __tablename__ = "files"
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(36), unique=True, index=True, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    path = Column(String(512), nullable=True)
    filename = Column(String(255), nullable=True)
    url = Column(String(512), nullable=True)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
