"""Profile visit: record visit."""
from datetime import datetime

from sqlalchemy.orm import Session

from app.db.models.profile_visit import ProfileVisit


class ProfileVisitService:
    def __init__(self, db: Session):
        self.db = db

    def record(self, visitor_id: int, profile_user_id: int) -> bool:
        try:
            if visitor_id == profile_user_id:
                return True
            v = ProfileVisit(visitor_id=visitor_id, profile_user_id=profile_user_id, created_at=datetime.utcnow())
            self.db.add(v)
            self.db.commit()
            return True
        except Exception:
            return False
