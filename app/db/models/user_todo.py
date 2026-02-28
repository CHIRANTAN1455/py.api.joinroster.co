"""User to-do item."""
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from app.db.base import Base


class UserTodo(Base):
    __tablename__ = "user_todos"
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(36), unique=True, index=True, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=True)
    done = Column(Integer, default=0)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
