"""User to-do CRUD."""
import uuid as uuid_lib
from datetime import datetime
from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

from app.db.models.user_todo import UserTodo


def _todo_resource(t: UserTodo) -> Dict[str, Any]:
    return {"uuid": t.uuid, "title": t.title, "done": t.done, "created_at": t.created_at}


class UserTodoService:
    def __init__(self, db: Session):
        self.db = db

    def list(self, user_id: int) -> List[Dict[str, Any]]:
        try:
            items = self.db.query(UserTodo).filter(UserTodo.user_id == user_id).order_by(UserTodo.created_at.desc()).all()
            return [_todo_resource(t) for t in items]
        except Exception:
            return []

    def get(self, uuid: str, user_id: int) -> Optional[Dict[str, Any]]:
        try:
            t = self.db.query(UserTodo).filter(UserTodo.uuid == uuid, UserTodo.user_id == user_id).first()
            return _todo_resource(t) if t else None
        except Exception:
            return None

    def create(self, user_id: int, payload: Any) -> Optional[Dict[str, Any]]:
        try:
            title = payload.get("title", "") if isinstance(payload, dict) else getattr(payload, "title", "")
            t = UserTodo(uuid=str(uuid_lib.uuid4()), user_id=user_id, title=title, done=0, created_at=datetime.utcnow(), updated_at=datetime.utcnow())
            self.db.add(t)
            self.db.commit()
            self.db.refresh(t)
            return _todo_resource(t)
        except Exception:
            return None

    def update(self, uuid: str, user_id: int, payload: Any) -> Optional[Dict[str, Any]]:
        try:
            t = self.db.query(UserTodo).filter(UserTodo.uuid == uuid, UserTodo.user_id == user_id).first()
            if not t:
                return None
            if isinstance(payload, dict):
                if "title" in payload:
                    t.title = payload["title"]
                if "done" in payload:
                    t.done = payload["done"]
            t.updated_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(t)
            return _todo_resource(t)
        except Exception:
            return None

    def delete(self, uuid: str, user_id: int) -> bool:
        try:
            t = self.db.query(UserTodo).filter(UserTodo.uuid == uuid, UserTodo.user_id == user_id).first()
            if not t:
                return False
            self.db.delete(t)
            self.db.commit()
            return True
        except Exception:
            return False
