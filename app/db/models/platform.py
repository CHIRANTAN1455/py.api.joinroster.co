from sqlalchemy import Column, DateTime, Integer, String

from app.db.base import Base


class Platform(Base):
    __tablename__ = "platforms"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(36), unique=True, index=True, nullable=True)
    icon = Column(String(255), nullable=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)
    active = Column(Integer, default=1)
    hide_from_customers = Column(Integer, default=0)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    deleted_at = Column(DateTime, nullable=True)
