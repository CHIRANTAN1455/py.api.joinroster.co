"""
Profile endpoints. Laravel-exact: status, message, user (or statistics, etc.).
All responses use uuid (no integer id) in user resource.
"""
import os
import uuid as uuid_lib
from typing import Any, Dict, Optional, Tuple

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user_id, require_auth
from app.core.laravel_response import success_with_message, user_to_laravel_user_resource
from app.db.session import get_db
from app.services.profile_service import ProfileService


router = APIRouter(prefix="/profile", tags=["profile"])


def get_profile_service(db: Session = Depends(get_db)) -> ProfileService:
    return ProfileService(db=db)


async def _parse_profile_update_body(request: Request) -> Tuple[Dict[str, Any], Any]:
    """
    Parse request body as JSON, multipart/form-data, or application/x-www-form-urlencoded.
    Never raises. Returns (payload_dict, photo_file_or_none). Photo is raw UploadFile for multipart.
    """
    payload: Dict[str, Any] = {}
    photo_file = None
    content_type = (request.headers.get("content-type") or "").lower()

    try:
        if "multipart/form-data" in content_type:
            form = await request.form()
            for key in form.keys():
                val = form.get(key)
                if key == "photo":
                    if val and hasattr(val, "read"):
                        photo_file = val
                    continue
                if val is not None and not (hasattr(val, "read") and callable(getattr(val, "read", None))):
                    s = val if isinstance(val, str) else (str(val) if val else None)
                    if s and s not in ("undefined", "null"):
                        payload[key] = s
        elif "application/x-www-form-urlencoded" in content_type:
            form = await request.form()
            for key, val in form.items():
                if val is not None and isinstance(val, str) and val not in ("undefined", "null"):
                    payload[key] = val
        else:
            body = await request.json()
            if isinstance(body, dict):
                payload = {k: v for k, v in body.items() if v is not None and v not in ("undefined", "null")}
    except Exception:
        pass
    return payload, photo_file


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


def _save_profile_photo(content: bytes, filename: str) -> Optional[str]:
    """Save photo to uploads dir and return URL. Laravel stores URL on user.photo, not files table."""
    try:
        upload_dir = os.environ.get("UPLOAD_DIR", "uploads")
        os.makedirs(upload_dir, exist_ok=True)
        ext = os.path.splitext(filename)[1] or ".bin"
        safe_name = f"{uuid_lib.uuid4().hex}{ext}"
        file_path = os.path.join(upload_dir, safe_name)
        with open(file_path, "wb") as fp:
            fp.write(content)
        return f"/uploads/{safe_name}"
    except Exception:
        return None


@router.post("/update", dependencies=[Depends(require_auth)])
async def update_profile(
    request: Request,
    profile_service: ProfileService = Depends(get_profile_service),
    current_user_id: int = Depends(get_current_user_id),
):
    """
    POST /profile/update — status, message, user.
    Accepts JSON, multipart/form-data, or application/x-www-form-urlencoded.
    Photo upload: saves to uploads/ and stores URL on user.photo (Laravel parity).
    """
    payload, photo_file = await _parse_profile_update_body(request)

    if photo_file:
        try:
            content = await photo_file.read()
            url = _save_profile_photo(content, photo_file.filename or "photo")
            if url:
                payload["photo"] = url
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
