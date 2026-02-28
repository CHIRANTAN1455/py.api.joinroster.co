"""Favourite CRUD."""
import uuid as uuid_lib
from datetime import datetime
from typing import Dict, List, Optional

from sqlalchemy.orm import Session

from app.core.laravel_response import user_to_laravel_user_resource
from app.db.models.favourite import Favourite
from app.db.models.user import User


def _favourite_resource(f: Favourite, editor: Optional[User] = None) -> Dict:
    return {"uuid": f.uuid, "editor": user_to_laravel_user_resource(editor) if editor else None, "created_at": f.created_at}


class FavouriteService:
    def __init__(self, db: Session):
        self.db = db

    def list(self, user_id: int) -> List[Dict]:
        try:
            items = self.db.query(Favourite).filter(Favourite.user_id == user_id).all()
            return [_favourite_resource(f, self.db.query(User).filter(User.id == f.editor_id).first()) for f in items]
        except Exception:
            return []

    def create(self, user_id: int, editor_uuid: str) -> Optional[Dict]:
        try:
            editor = self.db.query(User).filter(User.uuid == editor_uuid).first()
            if not editor:
                return None
            existing = self.db.query(Favourite).filter(Favourite.user_id == user_id, Favourite.editor_id == editor.id).first()
            if existing:
                return _favourite_resource(existing, editor)
            f = Favourite(uuid=str(uuid_lib.uuid4()), user_id=user_id, editor_id=editor.id, created_at=datetime.utcnow(), updated_at=datetime.utcnow())
            self.db.add(f)
            self.db.commit()
            self.db.refresh(f)
            return _favourite_resource(f, editor)
        except Exception:
            return None
