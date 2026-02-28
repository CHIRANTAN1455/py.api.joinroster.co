"""Matching endpoints. Laravel-exact: status, message, matching/creators. Path {id} = uuid, token as-is."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user_id, require_auth
from app.core.laravel_response import success_with_message
from app.db.session import get_db
from app.services.matching_service import MatchingService


router = APIRouter(prefix="/matching", tags=["matching"])


def get_matching_service(db: Session = Depends(get_db)) -> MatchingService:
    return MatchingService(db=db)


@router.get("", dependencies=[Depends(require_auth)])
def search_matching(
    page: int = Query(1, ge=1),
    service: MatchingService = Depends(get_matching_service),
    current_user_id: int = Depends(get_current_user_id),
):
    result = service.list_for_user(current_user_id, page=page)
    return success_with_message("Matching Loaded Successfully", matching=result["matching"], total=result["total"], page=result["page"])


@router.get("/project/{id}", dependencies=[Depends(require_auth)])
def get_matching_project(id: str, service: MatchingService = Depends(get_matching_service)):
    data = service.get_for_project(id)
    if not data:
        return {"status": "error", "matching": {}}
    return success_with_message("Matching Loaded Successfully", matching=data)


@router.patch("/editor", dependencies=[Depends(require_auth)])
def update_matching_editor(service: MatchingService = Depends(get_matching_service)):
    return success_with_message("Matching updated", matching={})


@router.get("/{id}")
def get_matching(id: str, service: MatchingService = Depends(get_matching_service)):
    data = service.get_by_uuid(id)
    if not data:
        return {"status": "error", "matching": {}}
    return success_with_message("Matching Loaded Successfully", matching=data)


@router.get("/token/{token}")
def get_matching_by_token(token: str, service: MatchingService = Depends(get_matching_service)):
    data = service.get_by_token(token)
    if not data:
        return {"status": "error", "matching": {}}
    return success_with_message("Matching Loaded Successfully", matching=data)


@router.post("", dependencies=[Depends(require_auth)])
def create_matching(
    service: MatchingService = Depends(get_matching_service),
    current_user_id: int = Depends(get_current_user_id),
):
    data = service.create(current_user_id, None, None)
    if not data:
        return {"status": "error", "message": "No project found", "matching": {}, "token": None}
    return success_with_message("Matching created", matching=data, token=data.get("token"))


@router.post("/creators", dependencies=[Depends(require_auth)])
def matching_creators(service: MatchingService = Depends(get_matching_service)):
    return success_with_message("Creators Loaded Successfully", creators=[])


@router.patch("/{id}", dependencies=[Depends(require_auth)])
def update_matching(id: str, service: MatchingService = Depends(get_matching_service)):
    data = service.update(id, None)
    if not data:
        return {"status": "error", "matching": {}}
    return success_with_message("Matching updated", matching=data)


@router.patch("/admin/{id}", dependencies=[Depends(require_auth)])
def admin_update_matching(id: str, service: MatchingService = Depends(get_matching_service)):
    data = service.update(id, None)
    if not data:
        return {"status": "error", "matching": {}}
    return success_with_message("Matching updated", matching=data)
