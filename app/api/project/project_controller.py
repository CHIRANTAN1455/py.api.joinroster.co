from typing import Any, Dict

from sqlalchemy.orm import Session

from app.api.project.schemas import (
    ProjectListResponse,
    ProjectMatchScoreResponse,
    ProjectResourceResponse,
)
from app.services.project_service import ProjectService


class ProjectController:
    """
    Controller functions corresponding to Laravel's ProjectController methods.
    """

    def __init__(self, db: Session):
        self.db = db
        self.service = ProjectService(db=db)

    def index(self, user_id: int, page: int = 1) -> ProjectListResponse:
        result = self.service.search(user_id=user_id, page=page)
        return ProjectListResponse(
            status="success",
            projects=result["projects"],
            total=result["total"],
            page=result["page"],
            metrics=result["metrics"],
        )

    def get(self, project_uuid: str) -> ProjectResourceResponse:
        project = self.service.get_by_uuid(uuid=project_uuid)
        if not project:
            # For now, return empty shape; detailed 404 behavior can be aligned
            # with Laravel later.
            return ProjectResourceResponse(status="error", project={})

        project_data: Dict[str, Any] = {
            "id": project.id,
            "uuid": project.uuid,
            "title": project.title,
            "description": project.description,
            "status": project.status,
        }
        return ProjectResourceResponse(status="success", project=project_data)

    def match_score(self, user_id: int, project_id: int) -> ProjectMatchScoreResponse:
        # Placeholder; real implementation will mirror ProjectService.calculateMatch.
        return ProjectMatchScoreResponse(
            status="success",
            match={"score": 0},
        )

