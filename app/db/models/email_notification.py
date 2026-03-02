from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text

from app.db.base import Base


class EmailNotification(Base):
    """
    Minimal SQLAlchemy representation of Laravel's `EmailNotification` model.

    We only model the fields touched by PdfSend:
      - id
      - uuid
      - name
      - code
      - subject
      - content
      - active
      - created_at
    The `tags` JSON column and other attributes are omitted for now.
    """

    __tablename__ = "email_notifications"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(36), unique=True, index=True, nullable=True)
    name = Column(String(255), nullable=True)
    code = Column(String(255), unique=True, nullable=False)
    subject = Column(String(255), nullable=True)
    content = Column(Text, nullable=True)
    active = Column(Boolean, default=True)

    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)

