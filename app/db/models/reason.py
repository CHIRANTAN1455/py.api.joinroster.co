from sqlalchemy import Column, DateTime, Integer, String, Text

from app.db.base import Base


class Reason(Base):
    __tablename__ = "reasons"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(36), unique=True, index=True, nullable=True)
    name = Column(String(255), nullable=True)
    tags = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    active = Column(Integer, default=1)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    deleted_at = Column(DateTime, nullable=True)
