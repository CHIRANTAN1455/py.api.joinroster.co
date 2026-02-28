import uuid as uuid_lib
from datetime import datetime
from typing import Any, Dict, List, Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.db.models.project import Project
from app.db.models.user import User


class ProjectService:
    """
    Laravel ProjectService parity: search (with metrics), create, update, cancel, get_by_uuid.
    """

    def __init__(self, db: Session):
        self.db = db

    def search(
        self,
        user_id: int,
        page: int = 1,
        per_page: int = 15,
        search: Optional[str] = None,
        status: Optional[str] = None,
    ) -> Dict[str, Any]:
        query = (
            self.db.query(Project)
            .filter(Project.deleted_at.is_(None))
            .filter(
                (Project.user_id == user_id) | (Project.editor_id == user_id)
            )
        )
        if search:
            q = f"%{search}%"
            query = query.filter(
                (Project.title.ilike(q)) | (Project.description.ilike(q))
            )
        if status:
            query = query.filter(Project.status == status)
        total = query.count()
        items: List[Project] = (
            query.order_by(Project.created_at.desc())
            .offset((page - 1) * per_page)
            .limit(per_page)
            .all()
        )
        projects_data = [
            {
                "uuid": p.uuid,
                "title": p.title,
                "description": p.description,
                "status": p.status,
            }
            for p in items
        ]
        metrics = self.status_metrics(user_id)
        return {
            "projects": projects_data,
            "total": total,
            "page": page,
            "metrics": metrics,
        }

    def status_metrics(self, user_id: int) -> Dict[str, int]:
        """Count projects by status for user (as owner or editor)."""
        rows = (
            self.db.query(Project.status, func.count(Project.id))
            .filter(Project.deleted_at.is_(None))
            .filter(
                (Project.user_id == user_id) | (Project.editor_id == user_id)
            )
            .group_by(Project.status)
            .all()
        )
        return {str(r[0] or "pending"): r[1] for r in rows}

    def get_by_uuid(self, uuid: str) -> Optional[Project]:
        return (
            self.db.query(Project)
            .filter(Project.uuid == uuid, Project.deleted_at.is_(None))
            .first()
        )

    def _get(self, payload: Any, key: str, default: Any = None) -> Any:
        if payload is None:
            return default
        if isinstance(payload, dict):
            return payload.get(key, default)
        return getattr(payload, key, default)

    def create(self, user_id: int, payload: Any) -> Optional[Project]:
        """Create project; payload dict or object with title, description, budget, editors, etc."""
        if payload is None:
            return None
        title = self._get(payload, "title") or ""
        description = self._get(payload, "description") or ""
        editor_id = None
        editors = self._get(payload, "editors") or []
        if editors and len(editors) > 0:
            first = editors[0]
            first_editor_uuid = first if isinstance(first, str) else self._get(first, "uuid")
            if first_editor_uuid:
                editor = self.db.query(User).filter(User.uuid == first_editor_uuid).first()
                if editor:
                    editor_id = editor.id
        project = Project(
            uuid=str(uuid_lib.uuid4()),
            user_id=user_id,
            editor_id=editor_id,
            title=title,
            description=description,
            budget=self._get(payload, "budget"),
            budget_per=self._get(payload, "budget_per") or "project",
            status=self._get(payload, "status") or "pending",
            published=self._get(payload, "published") or 0,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        return project

    def update(self, project_uuid: str, payload: Any) -> Optional[Project]:
        project = self.get_by_uuid(project_uuid)
        if not project or payload is None:
            return project
        title = self._get(payload, "title")
        if title is not None:
            project.title = title
        description = self._get(payload, "description")
        if description is not None:
            project.description = description
        if isinstance(payload, dict) and "budget" in payload:
            project.budget = payload["budget"]
        elif hasattr(payload, "model_fields_set") and "budget" in getattr(payload, "model_fields_set", set()):
            project.budget = self._get(payload, "budget")
        elif hasattr(payload, "budget"):
            project.budget = self._get(payload, "budget")
        status = self._get(payload, "status")
        if status is not None:
            project.status = status
        editor_uuid = self._get(payload, "editor_id") or (self._get(payload, "editors") or [None])[0]
        if editor_uuid:
            editor = self.db.query(User).filter(User.uuid == editor_uuid).first()
            if editor:
                project.editor_id = editor.id
        project.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(project)
        return project

    def cancel(self, project_uuid: str) -> Optional[Project]:
        project = self.get_by_uuid(project_uuid)
        if not project:
            return None
        project.status = "cancelled"
        project.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(project)
        return project

    def public_search(
        self, user_id: int, page: int = 1, per_page: int = 15
    ) -> Dict[str, Any]:
        """Public jobs (no editor assigned); same shape as search."""
        query = (
            self.db.query(Project)
            .filter(Project.deleted_at.is_(None), Project.editor_id.is_(None))
            .filter(Project.user_id == user_id)
        )
        total = query.count()
        items = (
            query.order_by(Project.created_at.desc())
            .offset((page - 1) * per_page)
            .limit(per_page)
            .all()
        )
        return {
            "projects": [
                {"uuid": p.uuid, "title": p.title, "description": p.description, "status": p.status}
                for p in items
            ],
            "total": total,
            "page": page,
        }

    def public_search_no_auth(self, page: int = 1, per_page: int = 15) -> Dict[str, Any]:
        query = (
            self.db.query(Project)
            .filter(Project.deleted_at.is_(None), Project.published == 1)
            .filter(Project.editor_id.is_(None))
        )
        total = query.count()
        items = (
            query.order_by(Project.created_at.desc())
            .offset((page - 1) * per_page)
            .limit(per_page)
            .all()
        )
        return {
            "projects": [
                {"uuid": p.uuid, "title": p.title, "description": p.description, "status": p.status}
                for p in items
            ],
            "total": total,
            "page": page,
        }

