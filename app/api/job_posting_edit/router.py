from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import require_auth
from app.core.laravel_response import success_with_message
from app.db.session import get_db
from app.services.project_service import ProjectService


router = APIRouter(prefix="/job-posting", tags=["job-posting-edit"])


def get_project_service(db: Session = Depends(get_db)) -> ProjectService:
    return ProjectService(db=db)


@router.patch("/edit/{uuid}", dependencies=[Depends(require_auth)])
def job_posting_edit(
    uuid: str,
    body: dict = None,
    service: ProjectService = Depends(get_project_service),
):
    project = service.update(uuid, body or {})
    if project:
        return success_with_message("Job posting updated", project={"uuid": project.uuid, "title": project.title, "status": project.status})
    return success_with_message("Job posting updated", project={})
