"""Editor: get by uuid, projects, creators, jobtypes, reviews, related. Editor = User."""
from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

from app.core.laravel_response import user_to_laravel_user_resource
from app.db.models.project import Project
from app.db.models.user import User


def _project_resource(p: Project) -> Dict[str, Any]:
    return {"uuid": p.uuid, "title": p.title, "description": p.description, "status": p.status}


class EditorService:
    def __init__(self, db: Session):
        self.db = db

    def get_editor(self, uuid: str) -> Optional[Dict[str, Any]]:
        user = self.db.query(User).filter(User.uuid == uuid).first()
        if not user:
            return None
        return user_to_laravel_user_resource(user)

    def get_projects(self, editor_uuid: str, page: int = 1, per_page: int = 15) -> Dict[str, Any]:
        user = self.db.query(User).filter(User.uuid == editor_uuid).first()
        if not user:
            return {"projects": [], "total": 0, "page": page}
        try:
            q = self.db.query(Project).filter(Project.deleted_at.is_(None), Project.editor_id == user.id)
            total = q.count()
            items = q.order_by(Project.created_at.desc()).offset((page - 1) * per_page).limit(per_page).all()
            return {"projects": [_project_resource(p) for p in items], "total": total, "page": page}
        except Exception:
            return {"projects": [], "total": 0, "page": page}

    def get_creators(self, editor_uuid: str) -> List[Dict[str, Any]]:
        user = self.db.query(User).filter(User.uuid == editor_uuid).first()
        if not user:
            return []
        project_user_ids = self.db.query(Project.user_id).filter(Project.editor_id == user.id).distinct().all()
        ids = [r[0] for r in project_user_ids if r[0]]
        if not ids:
            return []
        users = self.db.query(User).filter(User.id.in_(ids)).all()
        return [user_to_laravel_user_resource(u) for u in users]

    def get_jobtypes(self, editor_uuid: str) -> List[Dict[str, Any]]:
        return []

    def get_reviews(self, editor_uuid: str) -> List[Dict[str, Any]]:
        return []

    def get_related(self, editor_uuid: str) -> List[Dict[str, Any]]:
        try:
            user = self.db.query(User).filter(User.uuid == editor_uuid).first()
            if not user:
                return []
            q = self.db.query(User).filter(User.id != user.id, User.active.is_(True)).limit(10)
            return [user_to_laravel_user_resource(u) for u in q.all()]
        except Exception:
            return []
