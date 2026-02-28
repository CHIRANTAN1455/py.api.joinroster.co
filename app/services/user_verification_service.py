"""User verification CRUD."""
import uuid as uuid_lib
from datetime import datetime
from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

from app.db.models.user_verification import UserVerification


def _verification_resource(v: UserVerification) -> Dict[str, Any]:
    return {"uuid": v.uuid, "token": v.token, "type": v.type, "expires_at": v.expires_at, "created_at": v.created_at}


class UserVerificationService:
    def __init__(self, db: Session):
        self.db = db

    def list(self, user_id: int) -> List[Dict[str, Any]]:
        try:
            items = self.db.query(UserVerification).filter(UserVerification.user_id == user_id).all()
            return [_verification_resource(v) for v in items]
        except Exception:
            return []

    def create(self, user_id: int, payload: Any = None) -> Optional[Dict[str, Any]]:
        try:
            v = UserVerification(uuid=str(uuid_lib.uuid4()), user_id=user_id, token=str(uuid_lib.uuid4()), type="email", created_at=datetime.utcnow(), updated_at=datetime.utcnow())
            self.db.add(v)
            self.db.commit()
            self.db.refresh(v)
            return _verification_resource(v)
        except Exception:
            return None

    def delete(self, uuid: str, user_id: int) -> bool:
        try:
            v = self.db.query(UserVerification).filter(UserVerification.uuid == uuid, UserVerification.user_id == user_id).first()
            if not v:
                return False
            self.db.delete(v)
            self.db.commit()
            return True
        except Exception:
            return False
