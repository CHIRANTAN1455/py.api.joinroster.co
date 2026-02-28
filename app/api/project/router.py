from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.project.project_controller import ProjectController
from app.core.dependencies import require_auth, get_current_user_id
from app.db.session import get_db


router = APIRouter(prefix="/project", tags=["project"])


def get_controller(db: Session = Depends(get_db)) -> ProjectController:
    return ProjectController(db=db)


@router.get("")
def list_projects(
    page: int = Query(1, ge=1),
    controller: ProjectController = Depends(get_controller),
    current_user_id: int = Depends(get_current_user_id),
):
    """
    GET /project — Laravel-exact: status, projects, total, page, metrics.
    """
    return controller.index(user_id=current_user_id, page=page)


@router.get("/{id}", dependencies=[Depends(require_auth)])
def get_project(
    id: str,
    controller: ProjectController = Depends(get_controller),
):
    """
    GET /project/{id} — Laravel-exact: status, project (ProjectResource).
    """
    return controller.get(project_uuid=id)


@router.get("/match-score", dependencies=[Depends(require_auth)])
def project_match_score(
    user_id: int = Query(...),
    project_id: int = Query(...),
    controller: ProjectController = Depends(get_controller),
):
    """
    GET /project/match-score — Laravel-exact: status, match.
    """
    return controller.match_score(user_id=user_id, project_id=project_id)

