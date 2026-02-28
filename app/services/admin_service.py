"""Admin: list editors, creators, projects; get by uuid; delete editor."""
from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

from app.core.laravel_response import user_to_laravel_user_resource
from app.db.models.project import Project
from app.db.models.user import User


def _project_resource(p: Project) -> Dict[str, Any]:
    return {"uuid": p.uuid, "title": p.title, "description": p.description, "status": p.status}


class AdminService:
    def __init__(self, db: Session):
        self.db = db

    def list_editors(self, page: int = 1, per_page: int = 15) -> Dict[str, Any]:
        try:
            q = self.db.query(User).filter(User.active.is_(True))
            total = q.count()
            items = q.offset((page - 1) * per_page).limit(per_page).all()
            editors = [user_to_laravel_user_resource(u) for u in items]
            return {"editors": editors, "total": total, "page": page}
        except Exception:
            return {"editors": [], "total": 0, "page": page}

    def get_editor(self, uuid: str) -> Optional[Dict[str, Any]]:
        user = self.db.query(User).filter(User.uuid == uuid).first()
        if not user:
            return None
        return user_to_laravel_user_resource(user)

    def list_creators(self, page: int = 1, per_page: int = 15) -> Dict[str, Any]:
        try:
            q = self.db.query(User).filter(User.active.is_(True))
            total = q.count()
            items = q.offset((page - 1) * per_page).limit(per_page).all()
            creators = [user_to_laravel_user_resource(u) for u in items]
            return {"creators": creators, "total": total, "page": page}
        except Exception:
            return {"creators": [], "total": 0, "page": page}

    def get_creator(self, uuid: str) -> Optional[Dict[str, Any]]:
        user = self.db.query(User).filter(User.uuid == uuid).first()
        if not user:
            return None
        return user_to_laravel_user_resource(user)

    def list_projects(self, page: int = 1, per_page: int = 15) -> Dict[str, Any]:
        try:
            q = self.db.query(Project).filter(Project.deleted_at.is_(None))
            total = q.count()
            items = q.order_by(Project.created_at.desc()).offset((page - 1) * per_page).limit(per_page).all()
            projects = [_project_resource(p) for p in items]
            return {"projects": projects, "total": total, "page": page}
        except Exception:
            return {"projects": [], "total": 0, "page": page}

    def get_project(self, uuid: str) -> Optional[Dict[str, Any]]:
        p = self.db.query(Project).filter(Project.uuid == uuid, Project.deleted_at.is_(None)).first()
        if not p:
            return None
        return _project_resource(p)

    def delete_editor_by_email(self, email: str) -> bool:
        user = self.db.query(User).filter(User.email == email).first()
        if not user:
            return False
        user.active = False
        self.db.commit()
        return True
