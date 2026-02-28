"""Project application endpoints. Laravel-exact: status, message, application/applications. Path {id} = uuid."""
from fastapi import APIRouter, Depends

from app.core.dependencies import require_auth, unlimited_rate
from app.core.laravel_response import success_with_message


router = APIRouter(prefix="/project-application", tags=["project-application"])


@router.get("", dependencies=[Depends(require_auth)])
def list_project_applications():
    return success_with_message("Applications Loaded Successfully", applications=[], total=0, page=1)


@router.get("/{id}", dependencies=[Depends(require_auth)])
def get_project_application(id: str):
    return success_with_message("Application Loaded Successfully", application={})


@router.post("/add", dependencies=[Depends(require_auth)])
def add_project_application():
    return success_with_message("Application Created Successfully", application={})


@router.patch("/{id}", dependencies=[Depends(require_auth)])
def update_project_application(id: str):
    return success_with_message("Application Updated Successfully", application={})


@router.post("/{id}/note", dependencies=[Depends(require_auth)])
def add_project_application_note(id: str):
    return success_with_message("Note created", application={})


@router.delete("/note/{id}", dependencies=[Depends(require_auth)])
def delete_project_application_note(id: str):
    return success_with_message("Note deleted")


@router.post("/rejection", dependencies=[Depends(require_auth), Depends(unlimited_rate)])
def project_application_rejection():
    return success_with_message("Rejection sent")
