"""Admin endpoints. Laravel-exact: status, message, editors/editor/creators/user/projects/project. id/email in path = uuid or email."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.dependencies import require_auth
from app.core.laravel_response import success_with_message
from app.db.session import get_db
from app.services.admin_service import AdminService


router = APIRouter(prefix="/admin", tags=["admin"])


def get_admin_service(db: Session = Depends(get_db)) -> AdminService:
    return AdminService(db=db)


@router.get("/editors", dependencies=[Depends(require_auth)])
def list_editors(
    page: int = Query(1, ge=1),
    service: AdminService = Depends(get_admin_service),
):
    result = service.list_editors(page=page)
    return success_with_message(
        "Editors Loaded Successfully",
        editors=result["editors"],
        total=result["total"],
        page=result["page"],
    )


@router.get("/editors/{id}", dependencies=[Depends(require_auth)])
def get_editor(id: str, service: AdminService = Depends(get_admin_service)):
    editor = service.get_editor(id)
    if not editor:
        return {"status": "error", "message": "Editor not found", "editor": {}}
    return success_with_message("Editor Loaded Successfully", editor=editor)


@router.get("/creators/{id}", dependencies=[Depends(require_auth)])
def get_creator(id: str, service: AdminService = Depends(get_admin_service)):
    user = service.get_creator(id)
    if not user:
        return {"status": "error", "message": "Creator not found", "user": {}}
    return success_with_message("Creator Loaded Successfully", user=user)


@router.get("/creators", dependencies=[Depends(require_auth)])
def list_creators(
    page: int = Query(1, ge=1),
    service: AdminService = Depends(get_admin_service),
):
    result = service.list_creators(page=page)
    return success_with_message(
        "Creators Loaded Successfully",
        creators=result["creators"],
        total=result["total"],
        page=result["page"],
    )


@router.get("/projects", dependencies=[Depends(require_auth)])
def list_projects(
    page: int = Query(1, ge=1),
    service: AdminService = Depends(get_admin_service),
):
    result = service.list_projects(page=page)
    return success_with_message(
        "Projects Loaded Successfully",
        projects=result["projects"],
        total=result["total"],
        page=result["page"],
    )


@router.get("/projects/{id}", dependencies=[Depends(require_auth)])
def get_project_admin(id: str, service: AdminService = Depends(get_admin_service)):
    project = service.get_project(id)
    if not project:
        return {"status": "error", "message": "Project not found", "project": {}}
    return success_with_message("Project Loaded Successfully", project=project)


@router.delete("/editors/{email}", dependencies=[Depends(require_auth)])
def delete_editor(email: str, service: AdminService = Depends(get_admin_service)):
    ok = service.delete_editor_by_email(email)
    if not ok:
        return {"status": "error", "message": "Editor not found"}
    return success_with_message("Editor Deleted Successfully")


@router.post("/users/email", dependencies=[Depends(require_auth)])
def admin_users_email(service: AdminService = Depends(get_admin_service)):
    return success_with_message("Success")

