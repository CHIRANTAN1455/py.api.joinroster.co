from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.project.project_controller import ProjectController
from app.api.project.schemas import (
    ProjectListResponse,
    ProjectMatchScoreResponse,
    ProjectResourceResponse,
)
from app.core.dependencies import require_auth
from app.db.session import get_db


router = APIRouter(prefix="/project", tags=["project"])


def get_controller(db: Session = Depends(get_db)) -> ProjectController:
    return ProjectController(db=db)


@router.get(
    "",
    dependencies=[Depends(require_auth)],
    response_model=ProjectListResponse,
)
def list_projects(
    page: int = Query(1, ge=1),
    controller: ProjectController = Depends(get_controller),
) -> ProjectListResponse:
    """
    GET /project

    Middlewares in Laravel: auth:sanctum
    """
    # NOTE: user_id extraction from JWT subject must be added to fully mirror Laravel.
    user_id = 0
    return controller.index(user_id=user_id, page=page)


@router.get(
    "/{id}",
    dependencies=[Depends(require_auth)],
    response_model=ProjectResourceResponse,
)
def get_project(
    id: str,
    controller: ProjectController = Depends(get_controller),
) -> ProjectResourceResponse:
    """
    GET /project/{id}

    Middlewares in Laravel: auth:sanctum
    """
    return controller.get(project_uuid=id)


@router.get(
    "/match-score",
    dependencies=[Depends(require_auth)],
    response_model=ProjectMatchScoreResponse,
)
def project_match_score(
    user_id: int = Query(...),
    project_id: int = Query(...),
    controller: ProjectController = Depends(get_controller),
) -> ProjectMatchScoreResponse:
    """
    GET /project/match-score

    Middlewares in Laravel: auth:sanctum
    """
    return controller.match_score(user_id=user_id, project_id=project_id)

