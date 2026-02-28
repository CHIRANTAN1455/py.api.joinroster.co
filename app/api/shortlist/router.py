"""Shortlist. Path {id} = uuid. Laravel-exact: status, message, shortlist/shortlists."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user_id, require_auth
from app.core.laravel_response import success_with_message
from app.db.session import get_db
from app.services.shortlist_service import ShortlistService


router = APIRouter(prefix="/shortlist", tags=["shortlist"])


def get_shortlist_service(db: Session = Depends(get_db)) -> ShortlistService:
    return ShortlistService(db=db)


@router.get("", dependencies=[Depends(require_auth)])
def list_shortlist(
    service: ShortlistService = Depends(get_shortlist_service),
    current_user_id: int = Depends(get_current_user_id),
):
    shortlist = service.list(current_user_id)
    return success_with_message("Shortlist Loaded Successfully", shortlist=shortlist)


@router.patch("/{id}", dependencies=[Depends(require_auth)])
def update_shortlist(
    id: str,
    body: dict = None,
    service: ShortlistService = Depends(get_shortlist_service),
    current_user_id: int = Depends(get_current_user_id),
):
    shortlist = service.update(id, current_user_id, body or {})
    if not shortlist:
        return {"status": "error", "shortlist": {}}
    return success_with_message("Shortlist Updated Successfully", shortlist=shortlist)


@router.delete("/{id}", dependencies=[Depends(require_auth)])
def delete_shortlist(
    id: str,
    service: ShortlistService = Depends(get_shortlist_service),
    current_user_id: int = Depends(get_current_user_id),
):
    ok = service.delete(id, current_user_id)
    if not ok:
        return {"status": "error", "message": "Shortlist not found"}
    return success_with_message("Shortlist Deleted Successfully")
