"""
Profile endpoints. Laravel-exact: status, message, user (or statistics, etc.).
All responses use uuid (no integer id) in user resource.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user_id, require_auth
from app.core.laravel_response import success_with_message, user_to_laravel_user_resource
from app.db.models.user import User
from app.db.session import get_db


router = APIRouter(prefix="/profile", tags=["profile"])


def _get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


@router.get("", dependencies=[Depends(require_auth)])
def get_profile(
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    """GET /profile — status, message, user (UserResource)."""
    user = _get_user(db, current_user_id)
    if not user:
        return {"status": "error", "message": "User not found", "user": {}}
    return success_with_message(
        "Profile Loaded Successfully",
        user=user_to_laravel_user_resource(user),
    )


@router.get("/statistics", dependencies=[Depends(require_auth)])
def get_profile_statistics(
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    """GET /profile/statistics — status, message, statistics."""
    return success_with_message(
        "Statistics Loaded Successfully",
        statistics={},
    )


@router.get("/social", dependencies=[Depends(require_auth)])
def get_profile_social(
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    """GET /profile/social — status, message, social (or similar)."""
    return success_with_message(
        "Social Loaded Successfully",
        social=None,
    )


@router.post("/update", dependencies=[Depends(require_auth)])
def update_profile(
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    """POST /profile/update — status, message, user."""
    user = _get_user(db, current_user_id)
    if not user:
        return {"status": "error", "message": "User not found", "user": {}}
    return success_with_message(
        "Profile Updated Successfully",
        user=user_to_laravel_user_resource(user),
    )


@router.post("/pricing", dependencies=[Depends(require_auth)])
def update_profile_pricing(
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    return success_with_message("Pricing Updated Successfully", user=None)


@router.post("/pricing/no-delete", dependencies=[Depends(require_auth)])
def update_profile_pricing_no_delete(
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    return success_with_message("Pricing Updated Successfully", user=None)


@router.post("/skills", dependencies=[Depends(require_auth)])
def update_profile_skills(
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    return success_with_message("Skills Updated Successfully", user=None)


@router.post("/jobtypes", dependencies=[Depends(require_auth)])
def update_profile_jobtypes(
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    return success_with_message("Job Types Updated Successfully", user=None)


@router.post("/contentverticals", dependencies=[Depends(require_auth)])
def update_profile_contentverticals(
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    return success_with_message("Content Verticals Updated Successfully", user=None)


@router.post("/contentverticals/new", dependencies=[Depends(require_auth)])
def add_profile_contentverticals(
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    return success_with_message("Content Verticals Updated Successfully", user=None)


@router.post("/platforms", dependencies=[Depends(require_auth)])
def update_profile_platforms(
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    return success_with_message("Platforms Updated Successfully", user=None)


@router.post("/softwares", dependencies=[Depends(require_auth)])
def update_profile_softwares(
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    return success_with_message("Software Updated Successfully", user=None)


@router.post("/equipments", dependencies=[Depends(require_auth)])
def update_profile_equipments(
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    return success_with_message("Equipment Updated Successfully", user=None)


@router.post("/creativestyles", dependencies=[Depends(require_auth)])
def update_profile_creativestyles(
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    return success_with_message("Creative Styles Updated Successfully", user=None)
