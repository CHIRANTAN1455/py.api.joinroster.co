"""User verification link/token."""
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from app.db.base import Base


class UserVerification(Base):
    __tablename__ = "user_verifications"
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(36), unique=True, index=True, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    token = Column(String(255), nullable=True)
    type = Column(String(50), nullable=True)
    expires_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
