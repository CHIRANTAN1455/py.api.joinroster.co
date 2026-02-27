from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

from app.db.models.project import Project


class ProjectService:
    """
    Python equivalent of Laravel's ProjectService.

    Only a subset of behaviors is implemented initially; all methods preserve
    the top-level response keys described in the migration spec.
    """

    def __init__(self, db: Session):
        self.db = db

    def search(self, user_id: int, page: int = 1, per_page: int = 15) -> Dict[str, Any]:
        query = self.db.query(Project).filter(Project.user_id == user_id)
        total = query.count()
        items: List[Project] = (
            query.order_by(Project.created_at.desc())
            .offset((page - 1) * per_page)
            .limit(per_page)
            .all()
        )

        projects_data = [
            {
                "id": p.id,
                "uuid": p.uuid,
                "title": p.title,
                "description": p.description,
                "status": p.status,
            }
            for p in items
        ]

        return {
            "projects": projects_data,
            "total": total,
            "page": page,
            "metrics": {},
        }

    def get_by_uuid(self, uuid: str) -> Optional[Project]:
        return self.db.query(Project).filter(Project.uuid == uuid).first()

