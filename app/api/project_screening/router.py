"""Project screening. projectUuid, questionUuid in path. Laravel-exact: status, message, questions/question."""
from fastapi import APIRouter, Depends

from app.core.dependencies import require_auth
from app.core.laravel_response import success_with_message


router = APIRouter(prefix="/project", tags=["project-screening"])


@router.get("/{projectUuid}/screening-questions", dependencies=[Depends(require_auth)])
def list_project_screening_questions(projectUuid: str):
    return success_with_message("Screening questions loaded", questions=[])


@router.post("/{projectUuid}/screening-questions", dependencies=[Depends(require_auth)])
def create_project_screening_question(projectUuid: str):
    return success_with_message("Screening question created", question={})


@router.get("/{projectUuid}/screening-questions/{questionUuid}", dependencies=[Depends(require_auth)])
def get_project_screening_question(projectUuid: str, questionUuid: str):
    return success_with_message("Screening question loaded", question={})


@router.patch("/{projectUuid}/screening-questions/{questionUuid}", dependencies=[Depends(require_auth)])
def update_project_screening_question(projectUuid: str, questionUuid: str):
    return success_with_message("Screening question updated", question={})


@router.delete("/{projectUuid}/screening-questions/{questionUuid}", dependencies=[Depends(require_auth)])
def delete_project_screening_question(projectUuid: str, questionUuid: str):
    return success_with_message("Screening question deleted")
