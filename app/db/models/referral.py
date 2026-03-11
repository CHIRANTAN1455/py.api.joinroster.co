from sqlalchemy import Column, DateTime, Integer, String

from app.db.base import Base


class Referral(Base):
    """
    Matches Laravel referrals table (2023_02_01_193314_create_referrals_table).
    Base migration has: id, uuid, icon, name, description, active, timestamps, softDeletes.
    Some DBs may have priority, require_input from later migrations - use getattr in resources.
    """
    __tablename__ = "referrals"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(36), unique=True, index=True, nullable=True)
    icon = Column(String(255), nullable=True)
    name = Column(String(255), nullable=True)
    description = Column(String(255), nullable=True)
    active = Column(Integer, default=1)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    deleted_at = Column(DateTime, nullable=True)
