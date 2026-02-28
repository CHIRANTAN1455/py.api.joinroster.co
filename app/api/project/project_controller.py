from typing import Any, Dict

from sqlalchemy.orm import Session

from app.services.project_service import ProjectService


def _project_to_laravel_resource(project: Any) -> Dict[str, Any]:
    """Build Laravel ProjectResource-shaped dict (exact keys/casing)."""
    return {
        "id": project.id,
        "uuid": project.uuid,
        "title": project.title,
        "description": project.description or None,
        "status": project.status,
    }


class ProjectController:
    """
    Controller functions corresponding to Laravel's ProjectController methods.
    Returns plain dicts so JSON matches Laravel exactly (key order, names).
    """

    def __init__(self, db: Session):
        self.db = db
        self.service = ProjectService(db=db)

    def index(self, user_id: int, page: int = 1) -> Dict[str, Any]:
        result = self.service.search(user_id=user_id, page=page)
        # Laravel index: status, projects, total, page, metrics (no message)
        return {
            "status": "success",
            "projects": result["projects"],
            "total": result["total"],
            "page": result["page"],
            "metrics": result["metrics"],
        }

    def get(self, project_uuid: str) -> Dict[str, Any]:
        project = self.service.get_by_uuid(uuid=project_uuid)
        if not project:
            return {"status": "error", "project": {}}
        return {
            "status": "success",
            "project": _project_to_laravel_resource(project),
        }

    def match_score(self, user_id: int, project_id: int) -> Dict[str, Any]:
        # Placeholder; real implementation will mirror ProjectService.calculateMatch.
        return {"status": "success", "match": {"score": 0}}

