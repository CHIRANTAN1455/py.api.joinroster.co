from sqlalchemy import Column, DateTime, Integer, String

from app.db.base import Base


class Referral(Base):
    __tablename__ = "referrals"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(36), unique=True, index=True, nullable=True)
    name = Column(String(255), nullable=True)
    description = Column(String(255), nullable=True)
    priority = Column(Integer, nullable=True)
    require_input = Column(Integer, nullable=True)
    active = Column(Integer, default=1)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    deleted_at = Column(DateTime, nullable=True)
