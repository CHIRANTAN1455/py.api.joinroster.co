"""Social profile link (e.g. LinkedIn)."""
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from app.db.base import Base


class SocialProfile(Base):
    __tablename__ = "social_profiles"
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(36), unique=True, index=True, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    provider = Column(String(50), nullable=True)
    profile_id = Column(String(255), nullable=True)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
