"""
User referral record: when a user signs up using another user's referral code.
Laravel: referral_codes or similar table linking referrer to referred user.
"""
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String

from app.db.base import Base


class ReferralRecord(Base):
    __tablename__ = "referral_records"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(36), unique=True, index=True, nullable=True)
    referrer_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    referred_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    code = Column(String(255), nullable=True)
    paid = Column(Integer, default=0)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
