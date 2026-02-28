"""Social endpoints. Path {id} = uuid. Laravel-exact: status, message, social/socials. Mounted with prefix /api."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user_id, require_auth
from app.core.laravel_response import success_with_message
from app.db.session import get_db
from app.services.social_service import SocialService


router = APIRouter(prefix="", tags=["social"])


def get_social_service(db: Session = Depends(get_db)) -> SocialService:
    return SocialService(db=db)


@router.get("/social", dependencies=[Depends(require_auth)])
def list_social(
    service: SocialService = Depends(get_social_service),
    current_user_id: int = Depends(get_current_user_id),
):
    social = service.list(current_user_id)
    return success_with_message("Social Loaded Successfully", social=social)


@router.get("/profile/social/content-topics", dependencies=[Depends(require_auth)])
def profile_social_content_topics():
    return success_with_message("Content Topics Loaded Successfully", topics=[])


@router.post("/social", dependencies=[Depends(require_auth)])
def create_social(
    body: dict = None,
    service: SocialService = Depends(get_social_service),
    current_user_id: int = Depends(get_current_user_id),
):
    social = service.create(current_user_id, body or {})
    return success_with_message("Social Created Successfully", social=social or {})


@router.delete("/social/{id}", dependencies=[Depends(require_auth)])
def delete_social(
    id: str,
    service: SocialService = Depends(get_social_service),
    current_user_id: int = Depends(get_current_user_id),
):
    ok = service.delete(id, current_user_id)
    if not ok:
        return {"status": "error", "message": "Social not found"}
    return success_with_message("Social Deleted Successfully")
