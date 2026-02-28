"""Project screening. projectUuid, questionUuid in path. Laravel-exact: status, message, questions/question."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import require_auth
from app.core.laravel_response import success_with_message
from app.db.session import get_db
from app.services.project_screening_service import ProjectScreeningService


router = APIRouter(prefix="/project", tags=["project-screening"])


def get_screening_service(db: Session = Depends(get_db)) -> ProjectScreeningService:
    return ProjectScreeningService(db=db)


@router.get("/{projectUuid}/screening-questions", dependencies=[Depends(require_auth)])
def list_project_screening_questions(projectUuid: str, service: ProjectScreeningService = Depends(get_screening_service)):
    questions = service.list(projectUuid)
    return success_with_message("Screening questions loaded", questions=questions)


@router.post("/{projectUuid}/screening-questions", dependencies=[Depends(require_auth)])
def create_project_screening_question(
    projectUuid: str,
    body: dict = None,
    service: ProjectScreeningService = Depends(get_screening_service),
):
    question = service.create(projectUuid, body or {})
    return success_with_message("Screening question created", question=question or {})


@router.get("/{projectUuid}/screening-questions/{questionUuid}", dependencies=[Depends(require_auth)])
def get_project_screening_question(
    projectUuid: str,
    questionUuid: str,
    service: ProjectScreeningService = Depends(get_screening_service),
):
    question = service.get(projectUuid, questionUuid)
    if not question:
        return {"status": "error", "question": {}}
    return success_with_message("Screening question loaded", question=question)


@router.patch("/{projectUuid}/screening-questions/{questionUuid}", dependencies=[Depends(require_auth)])
def update_project_screening_question(
    projectUuid: str,
    questionUuid: str,
    body: dict = None,
    service: ProjectScreeningService = Depends(get_screening_service),
):
    question = service.update(projectUuid, questionUuid, body or {})
    if not question:
        return {"status": "error", "question": {}}
    return success_with_message("Screening question updated", question=question)


@router.delete("/{projectUuid}/screening-questions/{questionUuid}", dependencies=[Depends(require_auth)])
def delete_project_screening_question(
    projectUuid: str,
    questionUuid: str,
    service: ProjectScreeningService = Depends(get_screening_service),
):
    ok = service.delete(projectUuid, questionUuid)
    if not ok:
        return {"status": "error", "message": "Question not found"}
    return success_with_message("Screening question deleted")
