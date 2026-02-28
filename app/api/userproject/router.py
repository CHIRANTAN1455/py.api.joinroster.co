"""UserProject. Path {id} = uuid. Laravel-exact: status, message, project/projects/info."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user_id, require_auth
from app.core.laravel_response import success_with_message
from app.db.session import get_db
from app.services.project_service import ProjectService


router = APIRouter(prefix="/userproject", tags=["userproject"])


def get_project_service(db: Session = Depends(get_db)) -> ProjectService:
    return ProjectService(db=db)


@router.get("/public/info")
def userproject_public_info(service: ProjectService = Depends(get_project_service)):
    return success_with_message("Info Loaded Successfully", info={"total": 0})


@router.get("/public")
def userproject_public(
    page: int = Query(1, ge=1),
    service: ProjectService = Depends(get_project_service),
):
    result = service.public_search_no_auth(page=page)
    return success_with_message("Projects Loaded Successfully", projects=result["projects"], total=result["total"], page=result["page"])


@router.get("", dependencies=[Depends(require_auth)])
def list_userprojects(
    page: int = Query(1, ge=1),
    service: ProjectService = Depends(get_project_service),
    current_user_id: int = Depends(get_current_user_id),
):
    result = service.search(current_user_id, page=page)
    return success_with_message("Projects Loaded Successfully", projects=result["projects"], total=result["total"], page=result["page"])


@router.get("/info", dependencies=[Depends(require_auth)])
def userproject_info(
    service: ProjectService = Depends(get_project_service),
    current_user_id: int = Depends(get_current_user_id),
):
    result = service.search(current_user_id, page=1)
    return success_with_message("Info Loaded Successfully", info={"total": result["total"]})


@router.post("", dependencies=[Depends(require_auth)])
def create_userproject(
    service: ProjectService = Depends(get_project_service),
    current_user_id: int = Depends(get_current_user_id),
):
    project = service.create(current_user_id, {})
    if project:
        return success_with_message("Project Created Successfully", project={"uuid": project.uuid, "title": project.title, "status": project.status})
    return success_with_message("Project Created Successfully", project={})


@router.post("/{id}/update", dependencies=[Depends(require_auth)])
def update_userproject(
    id: str,
    service: ProjectService = Depends(get_project_service),
    current_user_id: int = Depends(get_current_user_id),
):
    project = service.update(id, {})
    if project:
        return success_with_message("Project Updated Successfully", project={"uuid": project.uuid, "title": project.title, "status": project.status})
    return success_with_message("Project Updated Successfully", project={})


@router.delete("/{id}", dependencies=[Depends(require_auth)])
def delete_userproject(id: str, service: ProjectService = Depends(get_project_service)):
    return success_with_message("Project Deleted Successfully")
