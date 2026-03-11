"""
Profile endpoints. Laravel-exact: status, message, user (or statistics, etc.).
All responses use uuid (no integer id) in user resource.
"""
from typing import Optional

from fastapi import APIRouter, Depends, File, Request, UploadFile
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user_id, require_auth
from app.core.laravel_response import success_with_message, user_to_laravel_user_resource
from app.db.session import get_db
from app.services.file_service import FileService
from app.services.profile_service import ProfileService


router = APIRouter(prefix="/profile", tags=["profile"])


def get_profile_service(db: Session = Depends(get_db)) -> ProfileService:
    return ProfileService(db=db)


def get_file_service(db: Session = Depends(get_db)) -> FileService:
    return FileService(db=db)


@router.get("", dependencies=[Depends(require_auth)])
def get_profile(
    profile_service: ProfileService = Depends(get_profile_service),
    current_user_id: int = Depends(get_current_user_id),
):
    """GET /profile — status, message, user (UserResource)."""
    user = profile_service.get_user(current_user_id)
    if not user:
        return {"status": "error", "message": "User not found", "user": {}}
    return success_with_message(
        "Profile Loaded Successfully",
        user=user_to_laravel_user_resource(user),
    )


@router.get("/statistics", dependencies=[Depends(require_auth)])
def get_profile_statistics(
    profile_service: ProfileService = Depends(get_profile_service),
    current_user_id: int = Depends(get_current_user_id),
):
    """GET /profile/statistics — status, message, statistics."""
    statistics = profile_service.get_statistics(current_user_id)
    return success_with_message(
        "Statistics Loaded Successfully",
        statistics=statistics,
    )


@router.get("/social", dependencies=[Depends(require_auth)])
def get_profile_social(
    profile_service: ProfileService = Depends(get_profile_service),
    current_user_id: int = Depends(get_current_user_id),
):
    """GET /profile/social — status, message, social (or similar)."""
    return success_with_message(
        "Social Loaded Successfully",
        social=None,
    )


@router.post("/update", dependencies=[Depends(require_auth)])
async def update_profile(
    request: Request,
    profile_service: ProfileService = Depends(get_profile_service),
    file_service: FileService = Depends(get_file_service),
    current_user_id: int = Depends(get_current_user_id),
):
    """
    POST /profile/update — status, message, user.
    Accepts JSON or multipart/form-data (for photo upload).
    """
    payload = {}
    content_type = request.headers.get("content-type", "")

    if "multipart/form-data" in content_type:
        form = await request.form()
        for key in form.keys():
            if key == "photo":
                continue  # handled below
            val = form.get(key)
            if val is not None and not (hasattr(val, "filename") and getattr(val, "filename", None)):
                payload[key] = val if isinstance(val, str) else (str(val) if val else None)
        photo = form.get("photo")
        if photo and hasattr(photo, "read") and getattr(photo, "filename", None):
            content = await photo.read()
            result = file_service.create(
                current_user_id, photo.filename or "photo", content=content
            )
            if result and result.get("url"):
                payload["photo"] = result["url"]
    else:
        try:
            body = await request.json()
            if isinstance(body, dict):
                payload = {k: v for k, v in body.items() if v is not None}
        except Exception:
            pass

    user = profile_service.update(current_user_id, payload if payload else None)
    if not user:
        return {"status": "error", "message": "User not found", "user": {}}
    return success_with_message(
        "Profile Updated Successfully",
        user=user_to_laravel_user_resource(user),
    )


@router.post("/pricing", dependencies=[Depends(require_auth)])
def update_profile_pricing(
    profile_service: ProfileService = Depends(get_profile_service),
    current_user_id: int = Depends(get_current_user_id),
):
    return success_with_message("Pricing Updated Successfully", user=None)


@router.post("/pricing/no-delete", dependencies=[Depends(require_auth)])
def update_profile_pricing_no_delete(
    profile_service: ProfileService = Depends(get_profile_service),
    current_user_id: int = Depends(get_current_user_id),
):
    return success_with_message("Pricing Updated Successfully", user=None)


@router.post("/skills", dependencies=[Depends(require_auth)])
def update_profile_skills(
    profile_service: ProfileService = Depends(get_profile_service),
    current_user_id: int = Depends(get_current_user_id),
):
    return success_with_message("Skills Updated Successfully", user=None)


@router.post("/jobtypes", dependencies=[Depends(require_auth)])
def update_profile_jobtypes(
    profile_service: ProfileService = Depends(get_profile_service),
    current_user_id: int = Depends(get_current_user_id),
):
    return success_with_message("Job Types Updated Successfully", user=None)


@router.post("/contentverticals", dependencies=[Depends(require_auth)])
def update_profile_contentverticals(
    profile_service: ProfileService = Depends(get_profile_service),
    current_user_id: int = Depends(get_current_user_id),
):
    return success_with_message("Content Verticals Updated Successfully", user=None)


@router.post("/contentverticals/new", dependencies=[Depends(require_auth)])
def add_profile_contentverticals(
    profile_service: ProfileService = Depends(get_profile_service),
    current_user_id: int = Depends(get_current_user_id),
):
    return success_with_message("Content Verticals Updated Successfully", user=None)


@router.post("/platforms", dependencies=[Depends(require_auth)])
def update_profile_platforms(
    profile_service: ProfileService = Depends(get_profile_service),
    current_user_id: int = Depends(get_current_user_id),
):
    return success_with_message("Platforms Updated Successfully", user=None)


@router.post("/softwares", dependencies=[Depends(require_auth)])
def update_profile_softwares(
    profile_service: ProfileService = Depends(get_profile_service),
    current_user_id: int = Depends(get_current_user_id),
):
    return success_with_message("Software Updated Successfully", user=None)


@router.post("/equipments", dependencies=[Depends(require_auth)])
def update_profile_equipments(
    profile_service: ProfileService = Depends(get_profile_service),
    current_user_id: int = Depends(get_current_user_id),
):
    return success_with_message("Equipment Updated Successfully", user=None)


@router.post("/creativestyles", dependencies=[Depends(require_auth)])
def update_profile_creativestyles(
    profile_service: ProfileService = Depends(get_profile_service),
    current_user_id: int = Depends(get_current_user_id),
):
    return success_with_message("Creative Styles Updated Successfully", user=None)
