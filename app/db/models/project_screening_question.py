"""Project screening question."""
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from app.db.base import Base


class ProjectScreeningQuestion(Base):
    __tablename__ = "project_screening_questions"
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(36), unique=True, index=True, nullable=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    question = Column(Text, nullable=True)
    order = Column(Integer, default=0)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
