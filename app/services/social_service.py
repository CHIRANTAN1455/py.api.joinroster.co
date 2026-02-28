"""Social profiles CRUD."""
import uuid as uuid_lib
from datetime import datetime
from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

from app.db.models.social_profile import SocialProfile


def _social_resource(s: SocialProfile) -> Dict[str, Any]:
    return {"uuid": s.uuid, "provider": s.provider, "profile_id": s.profile_id, "created_at": s.created_at}


class SocialService:
    def __init__(self, db: Session):
        self.db = db

    def list(self, user_id: int) -> List[Dict[str, Any]]:
        try:
            items = self.db.query(SocialProfile).filter(SocialProfile.user_id == user_id).all()
            return [_social_resource(s) for s in items]
        except Exception:
            return []

    def create(self, user_id: int, payload: Any) -> Optional[Dict[str, Any]]:
        try:
            provider = payload.get("provider", "") if isinstance(payload, dict) else getattr(payload, "provider", "")
            profile_id = payload.get("profile_id", "") if isinstance(payload, dict) else getattr(payload, "profile_id", "")
            s = SocialProfile(uuid=str(uuid_lib.uuid4()), user_id=user_id, provider=provider, profile_id=profile_id, created_at=datetime.utcnow(), updated_at=datetime.utcnow())
            self.db.add(s)
            self.db.commit()
            self.db.refresh(s)
            return _social_resource(s)
        except Exception:
            return None

    def delete(self, uuid: str, user_id: int) -> bool:
        try:
            s = self.db.query(SocialProfile).filter(SocialProfile.uuid == uuid, SocialProfile.user_id == user_id).first()
            if not s:
                return False
            self.db.delete(s)
            self.db.commit()
            return True
        except Exception:
            return False
