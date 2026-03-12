"""Project application endpoints. Laravel-exact: status, message, application/applications. Path {id} = uuid."""
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.project_application.schemas import (
    ProjectApplicationAddBody,
    ProjectApplicationNoteBody,
    ProjectApplicationRejectionBody,
    ProjectApplicationUpdateBody,
)
from app.core.dependencies import get_current_user_id, require_auth, unlimited_rate
from app.core.laravel_response import success_with_message
from app.db.session import get_db
from app.services.project_application_service import ProjectApplicationService


router = APIRouter(prefix="/project-application", tags=["project-application"])


def get_service(db: Session = Depends(get_db)) -> ProjectApplicationService:
    return ProjectApplicationService(db=db)


@router.get("", dependencies=[Depends(require_auth)])
@router.get("/", dependencies=[Depends(require_auth)], include_in_schema=False)
def list_project_applications(
    page: int = Query(1, ge=1),
    service: ProjectApplicationService = Depends(get_service),
    current_user_id: int = Depends(get_current_user_id),
):
    """
    Laravel ProjectApplicationController@index parity.

    Returns:
    {
      "status": "success",
      "message": "...",
      "project_applications": [...],
      "project": null,
      "page": <int>,
      "total": <int>
    }
    """
    result = service.list_for_user(current_user_id, page=page)
    return success_with_message(
        "Project applications loaded successfully",
        project_applications=result["applications"],
        project=None,
        page=result["page"],
        total=result["total"],
    )


@router.get("/{id}", dependencies=[Depends(require_auth)])
def get_project_application(
    id: str,
    service: ProjectApplicationService = Depends(get_service),
    current_user_id: int = Depends(get_current_user_id),
):
    """
    Laravel ProjectApplicationController@get parity.

    Returns:
    {
      "status": "success",
      "message": "...",
      "project_application": {...}
    }
    """
    data = service.get_application_response(id, current_user_id)
    if not data:
        return {
            "status": "error",
            "message": "Application not found",
            "project_application": {},
        }
    return success_with_message(
        "Project application loaded successfully",
        project_application=data,
    )


@router.post("/add", dependencies=[Depends(require_auth)])
def add_project_application(
    body: Optional[ProjectApplicationAddBody] = None,
    service: ProjectApplicationService = Depends(get_service),
    current_user_id: int = Depends(get_current_user_id),
):
    """
    Laravel ProjectApplicationController@store parity.

    On success:
    {
      "status": "success",
      "message": "...",
      "project_application": {...}
    }
    """
    project_uuid = body.project_uuid if body else None
    if not project_uuid:
        return {
            "status": "error",
            "message": "project_uuid required",
            "project_application": {},
        }
    app = service.create(current_user_id, project_uuid, body)
    if not app:
        return {
            "status": "error",
            "message": "Project not found or already applied",
            "project_application": {},
        }
    data = service.get_application_response(str(app.uuid), current_user_id)
    return success_with_message(
        "Project application created successfully",
        project_application=data,
    )


@router.patch("/{id}", dependencies=[Depends(require_auth)])
def update_project_application(
    id: str,
    body: Optional[ProjectApplicationUpdateBody] = None,
    service: ProjectApplicationService = Depends(get_service),
    current_user_id: int = Depends(get_current_user_id),
):
    """
    Laravel ProjectApplicationController@update parity.
    """
    payload = body.model_dump(exclude_unset=True) if body else None
    app = service.update(id, current_user_id, payload)
    if not app:
        return {
            "status": "error",
            "message": "Application not found",
            "project_application": {},
        }
    data = service.get_application_response(id, current_user_id)
    return success_with_message(
        "Project application updated successfully",
        project_application=data,
    )


@router.post("/{id}/note", dependencies=[Depends(require_auth)])
def add_project_application_note(
    id: str,
    body: Optional[ProjectApplicationNoteBody] = None,
    service: ProjectApplicationService = Depends(get_service),
    current_user_id: int = Depends(get_current_user_id),
):
    """
    Laravel ProjectApplicationController@create_note parity.
    """
    note = body.note if body and body.note else ""
    app = service.add_note(id, current_user_id, note)
    if not app:
        return {
            "status": "error",
            "message": "Application not found",
            "project_application": {},
        }
    data = service.get_application_response(id, current_user_id)
    return success_with_message(
        "Project application note created successfully",
        project_application=data,
    )


@router.delete("/note/{id}", dependencies=[Depends(require_auth)])
def delete_project_application_note(
    id: str,
    service: ProjectApplicationService = Depends(get_service),
    current_user_id: int = Depends(get_current_user_id),
):
    """
    Laravel ProjectApplicationController@delete_note parity.
    """
    ok = service.delete_note(id, current_user_id)
    if not ok:
        return {"status": "error", "message": "Note/Application not found"}
    return success_with_message(
        "Project application note deleted successfully",
    )


@router.post("/rejection", dependencies=[Depends(require_auth), Depends(unlimited_rate)])
def project_application_rejection(
    body: Optional[ProjectApplicationRejectionBody] = None,
    service: ProjectApplicationService = Depends(get_service),
    current_user_id: int = Depends(get_current_user_id),
):
    payload = body.model_dump() if body else None
    ok = service.reject(payload, current_user_id)
    if not ok:
        return {"status": "error", "message": "Application not found or not authorized"}
    return success_with_message("Rejection sent")
