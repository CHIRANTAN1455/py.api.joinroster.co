"""
Project routes. All {id} path params are project uuid (query by uuid).
Responses: status, message (where Laravel has it), project/projects/result/review/feedback/match.
No integer id in responses — uuid only.
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.project.project_controller import ProjectController
from app.core.dependencies import require_auth, get_current_user_id
from app.core.laravel_response import success_with_message
from app.db.session import get_db


router = APIRouter(prefix="/project", tags=["project"])


def get_controller(db: Session = Depends(get_db)) -> ProjectController:
    return ProjectController(db=db)


# ——— Public / no-auth (no require_auth) ———
@router.get("/public/metadata/{id}/no-auth")
def get_public_metadata_no_auth(id: str, controller: ProjectController = Depends(get_controller)):
    """id = project uuid."""
    return controller.get_public_metadata(project_uuid=id)


@router.get("/public/{id}/no-auth")
def get_public_project_no_auth(id: str, controller: ProjectController = Depends(get_controller)):
    return controller.get_public(project_uuid=id)


@router.get("/hackathon/{id}/no-auth")
def get_hackathon_no_auth(id: str, controller: ProjectController = Depends(get_controller)):
    return controller.get_hackathon(project_uuid=id)


@router.get("/public/no-auth")
def get_public_projects_no_auth(controller: ProjectController = Depends(get_controller)):
    return controller.list_public_no_auth()


# ——— Auth required ———
@router.get("")
def list_projects(
    page: int = Query(1, ge=1),
    controller: ProjectController = Depends(get_controller),
    current_user_id: int = Depends(get_current_user_id),
):
    return controller.index(user_id=current_user_id, page=page)


@router.get("/hackathon/{id}", dependencies=[Depends(require_auth)])
def get_hackathon(id: str, controller: ProjectController = Depends(get_controller)):
    return controller.get_hackathon(project_uuid=id)


@router.get("/match-score", dependencies=[Depends(require_auth)])
def project_match_score(
    user_id: int = Query(...),
    project_id: int = Query(...),
    controller: ProjectController = Depends(get_controller),
):
    return controller.match_score(user_id=user_id, project_id=project_id)


@router.post("/alert", dependencies=[Depends(require_auth)])
def project_alert(
    controller: ProjectController = Depends(get_controller),
    current_user_id: int = Depends(get_current_user_id),
):
    return success_with_message("Project alert sent", result=None)


@router.post("/alerts/2-days", dependencies=[Depends(require_auth)])
def project_alerts_2_days(
    controller: ProjectController = Depends(get_controller),
    current_user_id: int = Depends(get_current_user_id),
):
    return success_with_message("Project alerts sent", result=None)


@router.get("/public", dependencies=[Depends(require_auth)])
def get_public_projects(
    controller: ProjectController = Depends(get_controller),
    current_user_id: int = Depends(get_current_user_id),
):
    return controller.list_public(user_id=current_user_id)


@router.post("/add", dependencies=[Depends(require_auth)])
def project_add(
    controller: ProjectController = Depends(get_controller),
    current_user_id: int = Depends(get_current_user_id),
):
    return controller.store(user_id=current_user_id, payload=None)


@router.post("/public/add", dependencies=[Depends(require_auth)])
def project_public_add(
    controller: ProjectController = Depends(get_controller),
    current_user_id: int = Depends(get_current_user_id),
):
    return controller.store_public(user_id=current_user_id, payload=None)


@router.patch("/{id}", dependencies=[Depends(require_auth)])
def update_project(id: str, controller: ProjectController = Depends(get_controller)):
    return controller.update(project_uuid=id, payload=None)


@router.patch("/public/{id}", dependencies=[Depends(require_auth)])
def update_public_project(id: str, controller: ProjectController = Depends(get_controller)):
    return controller.update_public(project_uuid=id, payload=None)


@router.get("/{id}", dependencies=[Depends(require_auth)])
def get_project(id: str, controller: ProjectController = Depends(get_controller)):
    return controller.get(project_uuid=id)


@router.get("/public/{id}", dependencies=[Depends(require_auth)])
def get_public_project(id: str, controller: ProjectController = Depends(get_controller)):
    return controller.get_public(project_uuid=id)


@router.post("/hackathon/public/{id}", dependencies=[Depends(require_auth)])
def update_hackathon_public(id: str, controller: ProjectController = Depends(get_controller)):
    return controller.update_hackathon_public(project_uuid=id, payload=None)


@router.post("/{id}/cancel", dependencies=[Depends(require_auth)])
def project_cancel(id: str, controller: ProjectController = Depends(get_controller)):
    return controller.cancel(project_uuid=id, payload=None)


@router.post("/{id}/response", dependencies=[Depends(require_auth)])
def project_response(id: str, controller: ProjectController = Depends(get_controller)):
    return controller.response(project_uuid=id, payload=None)


@router.post("/{id}/status", dependencies=[Depends(require_auth)])
def project_status(id: str, controller: ProjectController = Depends(get_controller)):
    return controller.status(project_uuid=id, payload=None)


@router.post("/{id}/milestone", dependencies=[Depends(require_auth)])
def project_milestone(id: str, controller: ProjectController = Depends(get_controller)):
    return controller.milestone(project_uuid=id, payload=None)


@router.post("/{id}/deposit", dependencies=[Depends(require_auth)])
def project_deposit(id: str, controller: ProjectController = Depends(get_controller)):
    return controller.deposit(project_uuid=id, payload=None)


@router.post("/{id}/purchase", dependencies=[Depends(require_auth)])
def project_purchase(id: str, controller: ProjectController = Depends(get_controller)):
    return controller.purchase(project_uuid=id, payload=None)


@router.post("/{id}/review", dependencies=[Depends(require_auth)])
def project_review(id: str, controller: ProjectController = Depends(get_controller)):
    return controller.review(project_uuid=id, payload=None)


@router.post("/{id}/feedback", dependencies=[Depends(require_auth)])
def project_feedback(id: str, controller: ProjectController = Depends(get_controller)):
    return controller.feedback(project_uuid=id, payload=None)


@router.get("/{id}/conversation", dependencies=[Depends(require_auth)])
def project_conversation(id: str, controller: ProjectController = Depends(get_controller)):
    return controller.conversation(project_uuid=id)

