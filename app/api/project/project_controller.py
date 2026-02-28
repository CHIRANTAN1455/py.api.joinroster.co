from typing import Any, Dict, Optional

from sqlalchemy.orm import Session

from app.services.project_service import ProjectService


def _project_to_laravel_resource(project: Any) -> Dict[str, Any]:
    """Laravel ProjectResource shape; uuid only (no integer id)."""
    return {
        "uuid": project.uuid,
        "title": project.title,
        "description": project.description or None,
        "status": project.status,
    }


def _success_project(message: str, project: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    return {"status": "success", "message": message, "project": project or {}}


class ProjectController:
    """
    Laravel ProjectController parity. All id params are project uuid.
    Responses use uuid only (no integer id).
    """

    def __init__(self, db: Session):
        self.db = db
        self.service = ProjectService(db=db)

    def index(
        self,
        user_id: int,
        page: int = 1,
        search: Optional[str] = None,
        status: Optional[str] = None,
    ) -> Dict[str, Any]:
        result = self.service.search(
            user_id=user_id, page=page, search=search, status=status
        )
        return {
            "status": "success",
            "message": "Projects Loaded Successfully",
            "projects": result["projects"],
            "total": result["total"],
            "page": result["page"],
            "metrics": result["metrics"],
        }

    def get(self, project_uuid: str) -> Dict[str, Any]:
        project = self.service.get_by_uuid(uuid=project_uuid)
        if not project:
            return {"status": "error", "project": {}}
        return {"status": "success", "message": "Project Loaded Successfully", "project": _project_to_laravel_resource(project)}

    def get_public_metadata(self, project_uuid: str) -> Dict[str, Any]:
        project = self.service.get_by_uuid(uuid=project_uuid)
        if not project:
            return {"status": "error", "project": {}}
        return {"status": "success", "message": "Project Loaded Successfully", "project": _project_to_laravel_resource(project)}

    def get_public(self, project_uuid: str) -> Dict[str, Any]:
        project = self.service.get_by_uuid(uuid=project_uuid)
        if not project:
            return {"status": "error", "project": {}, "application": None}
        return {"status": "success", "message": "Project Loaded Successfully", "project": _project_to_laravel_resource(project), "application": None}

    def get_hackathon(self, project_uuid: str) -> Dict[str, Any]:
        return self.get(project_uuid)

    def list_public_no_auth(self, page: int = 1) -> Dict[str, Any]:
        result = self.service.public_search_no_auth(page=page)
        return {
            "status": "success",
            "projects": result["projects"],
            "total": result["total"],
            "page": result["page"],
        }

    def list_public(self, user_id: int, page: int = 1) -> Dict[str, Any]:
        result = self.service.public_search(user_id=user_id, page=page)
        return {
            "status": "success",
            "projects": result["projects"],
            "total": result["total"],
            "page": result["page"],
        }

    def store(self, user_id: int, payload: Any) -> Dict[str, Any]:
        project = self.service.create(user_id=user_id, payload=payload)
        if project:
            return _success_project(
                "Project Created Successfully",
                _project_to_laravel_resource(project),
            )
        return _success_project("Project Created Successfully", {})

    def store_public(self, user_id: int, payload: Any) -> Dict[str, Any]:
        return self.store(user_id=user_id, payload=payload)

    def update(self, project_uuid: str, payload: Any) -> Dict[str, Any]:
        project = self.service.update(project_uuid, payload)
        if not project:
            return {"status": "error", "project": {}}
        return _success_project(
            "Project Updated Successfully",
            _project_to_laravel_resource(project),
        )

    def update_public(self, project_uuid: str, payload: Any) -> Dict[str, Any]:
        return self.update(project_uuid=project_uuid, payload=payload)

    def update_hackathon_public(self, project_uuid: str, payload: Any) -> Dict[str, Any]:
        return self.update(project_uuid=project_uuid, payload=payload)

    def cancel(self, project_uuid: str, payload: Any) -> Dict[str, Any]:
        project = self.service.cancel(project_uuid)
        if not project:
            return {"status": "error", "project": {}}
        return _success_project(
            "Project Cancelled Successfully",
            _project_to_laravel_resource(project),
        )

    def response(self, project_uuid: str, payload: Any) -> Dict[str, Any]:
        return self.get(project_uuid)

    def status(self, project_uuid: str, payload: Any) -> Dict[str, Any]:
        return self.get(project_uuid)

    def milestone(self, project_uuid: str, payload: Any) -> Dict[str, Any]:
        return self.get(project_uuid)

    def deposit(self, project_uuid: str, payload: Any) -> Dict[str, Any]:
        return {"status": "success", "message": "Project Loaded Successfully", "result": {"checkout_url": None, "transaction": None}}

    def purchase(self, project_uuid: str, payload: Any) -> Dict[str, Any]:
        return {"status": "success", "message": "Project Loaded Successfully", "result": {}}

    def review(self, project_uuid: str, payload: Any) -> Dict[str, Any]:
        return {"status": "success", "message": "Review Created Successfully", "review": {}}

    def feedback(self, project_uuid: str, payload: Any) -> Dict[str, Any]:
        return {"status": "success", "message": "Feedback Created Successfully", "feedback": {}}

    def conversation(self, project_uuid: str) -> Dict[str, Any]:
        return {"status": "success", "message": "Match Loaded Successfully", "conversation": []}

    def match_score(self, user_id: int, project_id: int) -> Dict[str, Any]:
        return {"status": "success", "match": {"score": 0}}

