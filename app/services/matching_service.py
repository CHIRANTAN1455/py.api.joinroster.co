"""Matching: create, list, get by id/token, update."""
import uuid as uuid_lib
from datetime import datetime
from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

from app.db.models.matching import Matching
from app.db.models.project import Project
from app.db.models.user import User


def _matching_resource(m: Matching, project: Optional[Project] = None, editor: Optional[User] = None) -> Dict[str, Any]:
    return {
        "uuid": m.uuid,
        "token": m.token,
        "status": m.status,
        "project": {"uuid": project.uuid, "title": project.title} if project else None,
        "editor": {"uuid": editor.uuid, "name": editor.name} if editor else None,
        "created_at": m.created_at,
    }


class MatchingService:
    def __init__(self, db: Session):
        self.db = db

    def list_for_user(self, user_id: int, page: int = 1, per_page: int = 15) -> Dict[str, Any]:
        try:
            q = self.db.query(Matching).join(Project).filter(Project.user_id == user_id)
            total = q.count()
            items = q.order_by(Matching.created_at.desc()).offset((page - 1) * per_page).limit(per_page).all()
            out = []
            for m in items:
                proj = self.db.query(Project).filter(Project.id == m.project_id).first()
                ed = self.db.query(User).filter(User.id == m.editor_id).first() if m.editor_id else None
                out.append(_matching_resource(m, proj, ed))
            return {"matching": out, "total": total, "page": page}
        except Exception:
            return {"matching": [], "total": 0, "page": page}

    def get_by_uuid(self, uuid: str) -> Optional[Dict[str, Any]]:
        try:
            m = self.db.query(Matching).filter(Matching.uuid == uuid).first()
            if not m:
                return None
            proj = self.db.query(Project).filter(Project.id == m.project_id).first()
            ed = self.db.query(User).filter(User.id == m.editor_id).first() if m.editor_id else None
            return _matching_resource(m, proj, ed)
        except Exception:
            return None

    def get_by_token(self, token: str) -> Optional[Dict[str, Any]]:
        try:
            m = self.db.query(Matching).filter(Matching.token == token).first()
            if not m:
                return None
            proj = self.db.query(Project).filter(Project.id == m.project_id).first()
            ed = self.db.query(User).filter(User.id == m.editor_id).first() if m.editor_id else None
            return _matching_resource(m, proj, ed)
        except Exception:
            return None

    def get_for_project(self, project_uuid: str) -> Optional[Dict[str, Any]]:
        try:
            proj = self.db.query(Project).filter(Project.uuid == project_uuid).first()
            if not proj:
                return None
            m = self.db.query(Matching).filter(Matching.project_id == proj.id).first()
            if not m:
                return None
            ed = self.db.query(User).filter(User.id == m.editor_id).first() if m.editor_id else None
            return _matching_resource(m, proj, ed)
        except Exception:
            return None

    def create(self, user_id: int, project_uuid: Optional[str] = None, payload: Any = None) -> Optional[Dict[str, Any]]:
        try:
            project = None
            if project_uuid:
                project = self.db.query(Project).filter(Project.uuid == project_uuid, Project.user_id == user_id).first()
            if not project:
                projs = self.db.query(Project).filter(Project.user_id == user_id).limit(1).all()
                project = projs[0] if projs else None
            if not project:
                return None
            token = str(uuid_lib.uuid4()).replace("-", "")[:16]
            m = Matching(
                uuid=str(uuid_lib.uuid4()),
                project_id=project.id,
                token=token,
                status="pending",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            self.db.add(m)
            self.db.commit()
            self.db.refresh(m)
            ed = self.db.query(User).filter(User.id == m.editor_id).first() if m.editor_id else None
            return _matching_resource(m, project, ed)
        except Exception:
            return None

    def update(self, uuid: str, payload: Any = None) -> Optional[Dict[str, Any]]:
        try:
            m = self.db.query(Matching).filter(Matching.uuid == uuid).first()
            if not m:
                return None
            if payload and isinstance(payload, dict) and "editor_id" in payload:
                m.editor_id = payload["editor_id"]
            m.updated_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(m)
            proj = self.db.query(Project).filter(Project.id == m.project_id).first()
            ed = self.db.query(User).filter(User.id == m.editor_id).first() if m.editor_id else None
            return _matching_resource(m, proj, ed)
        except Exception:
            return None
