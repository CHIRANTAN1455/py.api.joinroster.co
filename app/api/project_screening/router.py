from fastapi import APIRouter, Depends

from app.core.dependencies import require_auth


router = APIRouter(prefix="/project", tags=["project-screening"])


@router.get(
    "/{projectUuid}/screening-questions",
    dependencies=[Depends(require_auth)],
)
def list_project_screening_questions(projectUuid: str):
    return {"status": "success", "projectUuid": projectUuid}


@router.post(
    "/{projectUuid}/screening-questions",
    dependencies=[Depends(require_auth)],
)
def create_project_screening_question(projectUuid: str):
    return {"status": "success", "projectUuid": projectUuid}


@router.get(
    "/{projectUuid}/screening-questions/{questionUuid}",
    dependencies=[Depends(require_auth)],
)
def get_project_screening_question(projectUuid: str, questionUuid: str):
    return {"status": "success", "projectUuid": projectUuid, "questionUuid": questionUuid}


@router.patch(
    "/{projectUuid}/screening-questions/{questionUuid}",
    dependencies=[Depends(require_auth)],
)
def update_project_screening_question(projectUuid: str, questionUuid: str):
    return {"status": "success", "projectUuid": projectUuid, "questionUuid": questionUuid}


@router.delete(
    "/{projectUuid}/screening-questions/{questionUuid}",
    dependencies=[Depends(require_auth)],
)
def delete_project_screening_question(projectUuid: str, questionUuid: str):
    return {"status": "success", "projectUuid": projectUuid, "questionUuid": questionUuid}

