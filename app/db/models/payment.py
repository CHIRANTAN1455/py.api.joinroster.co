"""Payment record."""
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String
from app.db.base import Base


class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(36), unique=True, index=True, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    amount = Column(Numeric(12, 2), nullable=True)
    status = Column(String(50), nullable=True)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
