from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user_id, require_auth
from app.core.laravel_response import success_with_message
from app.db.session import get_db
from app.services.profile_visit_service import ProfileVisitService


router = APIRouter(prefix="/profile-visit", tags=["profile-visit"])


def get_profile_visit_service(db: Session = Depends(get_db)) -> ProfileVisitService:
    return ProfileVisitService(db=db)


@router.post("", dependencies=[Depends(require_auth)])
def profile_visit(
    body: dict = None,
    service: ProfileVisitService = Depends(get_profile_visit_service),
    current_user_id: int = Depends(get_current_user_id),
):
    profile_user_id = body.get("profile_user_id", current_user_id) if body else current_user_id
    if isinstance(profile_user_id, str):
        from app.db.models.user import User
        user = service.db.query(User).filter(User.uuid == profile_user_id).first()  # noqa: S106
        profile_user_id = user.id if user else current_user_id
    service.record(current_user_id, int(profile_user_id))
    return success_with_message("Profile visit recorded")
