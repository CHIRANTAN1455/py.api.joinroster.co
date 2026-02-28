"""Shortlist CRUD."""
import uuid as uuid_lib
from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

from app.db.models.shortlist import Shortlist
from app.db.models.project import Project


def _shortlist_resource(s: Shortlist, project: Optional[Project] = None) -> Dict[str, Any]:
    return {
        "uuid": s.uuid,
        "project": {"uuid": project.uuid, "title": project.title} if project else None,
        "created_at": s.created_at,
    }


class ShortlistService:
    def __init__(self, db: Session):
        self.db = db

    def list(self, user_id: int) -> List[Dict[str, Any]]:
        try:
            items = self.db.query(Shortlist).filter(Shortlist.user_id == user_id).all()
            out = []
            for s in items:
                proj = self.db.query(Project).filter(Project.id == s.project_id).first() if s.project_id else None
                out.append(_shortlist_resource(s, proj))
            return out
        except Exception:
            return []

    def get(self, uuid: str, user_id: int) -> Optional[Dict[str, Any]]:
        try:
            s = self.db.query(Shortlist).filter(Shortlist.uuid == uuid, Shortlist.user_id == user_id).first()
            if not s:
                return None
            proj = self.db.query(Project).filter(Project.id == s.project_id).first() if s.project_id else None
            return _shortlist_resource(s, proj)
        except Exception:
            return None

    def update(self, uuid: str, user_id: int, payload: Any) -> Optional[Dict[str, Any]]:
        try:
            s = self.db.query(Shortlist).filter(Shortlist.uuid == uuid, Shortlist.user_id == user_id).first()
            if not s:
                return None
            if isinstance(payload, dict) and "project_id" in payload:
                s.project_id = payload["project_id"]
            self.db.commit()
            self.db.refresh(s)
            proj = self.db.query(Project).filter(Project.id == s.project_id).first() if s.project_id else None
            return _shortlist_resource(s, proj)
        except Exception:
            return None

    def delete(self, uuid: str, user_id: int) -> bool:
        try:
            s = self.db.query(Shortlist).filter(Shortlist.uuid == uuid, Shortlist.user_id == user_id).first()
            if not s:
                return False
            self.db.delete(s)
            self.db.commit()
            return True
        except Exception:
            return False
