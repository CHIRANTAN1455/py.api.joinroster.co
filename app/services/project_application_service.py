"""Project application CRUD. Laravel parity."""
import uuid as uuid_lib
from datetime import datetime
from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

from app.db.models.project import Project
from app.db.models.project_application import ProjectApplication
from app.db.models.user import User


def _application_to_resource(app: ProjectApplication, project: Optional[Project] = None, user: Optional[User] = None) -> Dict[str, Any]:
    return {
        "uuid": app.uuid,
        "project_id": getattr(app, "project_id", None),
        "project": {"uuid": project.uuid, "title": project.title} if project else None,
        "user_id": getattr(app, "user_id", None),
        "user": {"uuid": user.uuid, "name": user.name, "email": user.email} if user else None,
        "status": app.status,
        "note": app.note,
        "created_at": app.created_at,
        "updated_at": app.updated_at,
    }


class ProjectApplicationService:
    def __init__(self, db: Session):
        self.db = db

    def list_for_user(self, user_id: int, page: int = 1, per_page: int = 15) -> Dict[str, Any]:
        try:
            q = (
                self.db.query(ProjectApplication)
                .filter(ProjectApplication.deleted_at.is_(None))
                .filter(ProjectApplication.user_id == user_id)
            )
            total = q.count()
            items = q.order_by(ProjectApplication.created_at.desc()).offset((page - 1) * per_page).limit(per_page).all()
            applications = []
            for app in items:
                proj = self.db.query(Project).filter(Project.id == app.project_id).first()
                usr = self.db.query(User).filter(User.id == app.user_id).first()
                applications.append(_application_to_resource(app, proj, usr))
            return {"applications": applications, "total": total, "page": page}
        except Exception:
            return {"applications": [], "total": 0, "page": page}

    def get_by_uuid(self, uuid: str, user_id: Optional[int] = None) -> Optional[ProjectApplication]:
        q = self.db.query(ProjectApplication).filter(ProjectApplication.uuid == uuid, ProjectApplication.deleted_at.is_(None))
        if user_id is not None:
            q = q.filter(ProjectApplication.user_id == user_id)
        return q.first()

    def get_application_response(self, uuid: str, user_id: int) -> Dict[str, Any]:
        app = self.get_by_uuid(uuid, user_id=user_id)
        if not app:
            return {}
        proj = self.db.query(Project).filter(Project.id == app.project_id).first()
        usr = self.db.query(User).filter(User.id == app.user_id).first()
        return _application_to_resource(app, proj, usr)

    def create(self, user_id: int, project_uuid: str, payload: Any = None) -> Optional[ProjectApplication]:
        project = self.db.query(Project).filter(Project.uuid == project_uuid, Project.deleted_at.is_(None)).first()
        if not project:
            return None
        existing = (
            self.db.query(ProjectApplication)
            .filter(ProjectApplication.project_id == project.id, ProjectApplication.user_id == user_id, ProjectApplication.deleted_at.is_(None))
            .first()
        )
        if existing:
            return existing
        app = ProjectApplication(
            uuid=str(uuid_lib.uuid4()),
            project_id=project.id,
            user_id=user_id,
            status="pending",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        self.db.add(app)
        self.db.commit()
        self.db.refresh(app)
        return app

    def update(self, uuid: str, user_id: int, payload: Any) -> Optional[ProjectApplication]:
        app = self.get_by_uuid(uuid, user_id=user_id)
        if not app or payload is None:
            return app
        if isinstance(payload, dict):
            if "status" in payload:
                app.status = payload["status"]
        elif hasattr(payload, "status"):
            app.status = payload.status
        app.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(app)
        return app

    def add_note(self, uuid: str, user_id: int, note: str) -> Optional[ProjectApplication]:
        app = self.get_by_uuid(uuid, user_id=user_id)
        if not app:
            return None
        app.note = note
        app.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(app)
        return app

    def delete_note(self, note_uuid: str, user_id: int) -> bool:
        app = self.get_by_uuid(note_uuid, user_id=user_id)
        if not app:
            return False
        app.note = None
        app.updated_at = datetime.utcnow()
        self.db.commit()
        return True

    def reject(self, payload: Any, user_id: int) -> bool:
        if not payload:
            return False
        app_uuid = payload.get("application_uuid") if isinstance(payload, dict) else getattr(payload, "application_uuid", None)
        if not app_uuid:
            return False
        app = self.db.query(ProjectApplication).filter(ProjectApplication.uuid == str(app_uuid), ProjectApplication.deleted_at.is_(None)).first()
        if not app:
            return False
        project = self.db.query(Project).filter(Project.id == app.project_id).first()
        if not project or project.user_id != user_id:
            return False
        app.status = "rejected"
        app.updated_at = datetime.utcnow()
        self.db.commit()
        return True
