"""Profile visit: track who visited whose profile."""
from sqlalchemy import Column, DateTime, ForeignKey, Integer
from app.db.base import Base


class ProfileVisit(Base):
    __tablename__ = "profile_visits"
    id = Column(Integer, primary_key=True, index=True)
    visitor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    profile_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, nullable=True)
