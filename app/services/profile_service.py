"""
Profile service: get user, update user, get statistics.
Laravel parity for profile endpoints.
"""
from datetime import datetime
from typing import Any, Dict, Optional

from sqlalchemy.orm import Session

from app.db.models.project import Project
from app.db.models.user import User


class ProfileService:
    def __init__(self, db: Session):
        self.db = db

    def _get(self, payload: Any, key: str, default: Any = None) -> Any:
        if payload is None:
            return default
        if isinstance(payload, dict):
            return payload.get(key, default)
        return getattr(payload, key, default)

    def get_user(self, user_id: int) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()

    def update(
        self,
        user_id: int,
        payload: Any,
    ) -> Optional[User]:
        """Update user profile from payload (first_name, last_name, email, phone, etc.)."""
        user = self.get_user(user_id)
        if not user or payload is None:
            return user
        allowed = ("first_name", "last_name", "name", "email", "phone", "username")
        for key in allowed:
            if not hasattr(user, key):
                continue
            val = self._get(payload, key)
            if val is not None:
                setattr(user, key, val)
        if not user.name and (user.first_name or user.last_name):
            user.name = f"{user.first_name or ''} {user.last_name or ''}".strip()
        user.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_statistics(self, user_id: int) -> Dict[str, Any]:
        """Return Laravel-style statistics (project counts, etc.)."""
        projects_count = (
            self.db.query(Project)
            .filter(Project.user_id == user_id, Project.deleted_at.is_(None))
            .count()
        )
        return {
            "projects_count": projects_count,
            "applications_count": 0,
        }
