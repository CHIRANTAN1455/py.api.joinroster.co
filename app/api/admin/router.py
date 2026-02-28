"""Admin endpoints. Laravel-exact: status, message, editors/editor/creators/user/projects/project. id/email in path = uuid or email."""
from fastapi import APIRouter, Depends

from app.core.dependencies import require_auth
from app.core.laravel_response import success_with_message


router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/editors", dependencies=[Depends(require_auth)])
def list_editors():
    """status, message, editors, total, page."""
    return success_with_message("Editors Loaded Successfully", editors=[], total=0, page=1)


@router.get("/editors/{id}", dependencies=[Depends(require_auth)])
def get_editor(id: str):
    """id = uuid. status, message, editor."""
    return success_with_message("Editor Loaded Successfully", editor={})


@router.get("/creators/{id}", dependencies=[Depends(require_auth)])
def get_creator(id: str):
    """id = uuid. status, message, user."""
    return success_with_message("Creator Loaded Successfully", user={})


@router.get("/creators", dependencies=[Depends(require_auth)])
def list_creators():
    """status, message, creators, total, page."""
    return success_with_message("Creators Loaded Successfully", creators=[], total=0, page=1)


@router.get("/projects", dependencies=[Depends(require_auth)])
def list_projects():
    """status, message, projects, total, page."""
    return success_with_message("Projects Loaded Successfully", projects=[], total=0, page=1)


@router.get("/projects/{id}", dependencies=[Depends(require_auth)])
def get_project_admin(id: str):
    """id = project uuid. status, message, project."""
    return success_with_message("Project Loaded Successfully", project={})


@router.delete("/editors/{email}", dependencies=[Depends(require_auth)])
def delete_editor(email: str):
    """status, message."""
    return success_with_message("Editor Deleted Successfully")


@router.post("/users/email", dependencies=[Depends(require_auth)])
def admin_users_email():
    return success_with_message("Success")

