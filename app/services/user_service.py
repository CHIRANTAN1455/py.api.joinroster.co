"""User API: get by uuid, update, timezone, policy, delete, referral lookup."""
from datetime import datetime
from typing import Any, Dict, Optional

from sqlalchemy.orm import Session

from app.db.models.user import User


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def get_by_uuid(self, uuid: str) -> Optional[User]:
        return self.db.query(User).filter(User.uuid == uuid).first()

    def _get(self, payload: Any, key: str, default: Any = None) -> Any:
        if payload is None:
            return default
        if isinstance(payload, dict):
            return payload.get(key, default)
        return getattr(payload, key, default)

    def update_by_uuid(self, user_uuid: str, current_user_id: int, payload: Any) -> Optional[User]:
        user = self.get_by_uuid(user_uuid)
        if not user or user.id != current_user_id:
            return None
        if payload is None:
            return user
        for key in ("first_name", "last_name", "name", "email", "phone", "username"):
            if hasattr(user, key):
                val = self._get(payload, key)
                if val is not None:
                    setattr(user, key, val)
        if not user.name and (user.first_name or user.last_name):
            user.name = f"{user.first_name or ''} {user.last_name or ''}".strip()
        user.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(user)
        return user

    def update_timezone(self, user_uuid: str, current_user_id: int, timezone: Optional[str] = None, utc_offset: Optional[str] = None) -> Optional[User]:
        user = self.get_by_uuid(user_uuid)
        if not user or user.id != current_user_id:
            return None
        if hasattr(user, "timezone") and timezone is not None:
            setattr(user, "timezone", timezone)
        if hasattr(user, "utc_offset") and utc_offset is not None:
            setattr(user, "utc_offset", utc_offset)
        user.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(user)
        return user

    def accept_policy(self, user_uuid: str, current_user_id: int) -> Optional[User]:
        user = self.get_by_uuid(user_uuid)
        if not user or user.id != current_user_id:
            return None
        user.policy_accepted = True
        user.policy_accepted_at = datetime.utcnow()
        if hasattr(user, "updated_at"):
            user.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete_by_uuid(self, user_uuid: str, current_user_id: int) -> bool:
        user = self.get_by_uuid(user_uuid)
        if not user or user.id != current_user_id:
            return False
        self.db.delete(user)
        self.db.commit()
        return True

    def get_referral_by_code(self, code: str) -> Dict[str, Any]:
        """Check if referral code is valid (e.g. belongs to a user). Returns referral info and valid=True/False."""
        if not code:
            return {"referral": {}, "valid": False}
        user = self.db.query(User).filter(User.username == code).first()
        if user:
            return {
                "referral": {"uuid": user.uuid, "name": user.name, "username": user.username},
                "valid": True,
            }
        return {"referral": {}, "valid": False}
