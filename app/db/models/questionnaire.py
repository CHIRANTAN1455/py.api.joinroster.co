"""Questionnaire and response."""
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from app.db.base import Base


class Questionnaire(Base):
    __tablename__ = "questionnaires"
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(36), unique=True, index=True, nullable=True)
    title = Column(String(255), nullable=True)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)


class QuestionnaireResponse(Base):
    __tablename__ = "questionnaire_responses"
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(36), unique=True, index=True, nullable=True)
    questionnaire_id = Column(Integer, ForeignKey("questionnaires.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    answers = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
