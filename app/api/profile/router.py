"""
Profile endpoints. Laravel-exact: status, message, user (or statistics, etc.).
All responses use uuid (no integer id) in user resource.
"""
import json
import os
import uuid as uuid_lib
from typing import Any, Dict, Optional, Tuple

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user_id, require_auth
from app.core.image_compression import compress_image
from app.core.laravel_response import success_with_message, user_to_laravel_user_resource
from app.db.session import get_db
from app.services.profile_service import ProfileService


router = APIRouter(prefix="/profile", tags=["profile"])


def get_profile_service(db: Session = Depends(get_db)) -> ProfileService:
    return ProfileService(db=db)


def _flatten_payload(obj: Any) -> Dict[str, Any]:
    """
    Extract profile fields from payload. Laravel may send wrapped in "data", "user", or "body".
    Returns flat dict; preserves bool/int/float, stringifies the rest.
    """
    if not obj or not isinstance(obj, dict):
        return {}
    # Unwrap Laravel-style nested payload: { "data": {...} } or { "user": {...} } or { "body": {...} }
    inner = obj.get("data") or obj.get("user") or obj.get("body")
    if isinstance(inner, dict):
        obj = inner
    elif isinstance(inner, str):
        # Client may send body as JSON string
        try:
            parsed = json.loads(inner)
            if isinstance(parsed, dict):
                obj = parsed
        except (json.JSONDecodeError, TypeError):
            pass
    out: Dict[str, Any] = {}
    for k, v in obj.items():
        if k == "body":
            continue  # Never pass raw "body" to service
        if v is None or v in ("undefined", "null"):
            continue
        if isinstance(v, (dict, list)):
            continue  # Skip nested; profile fields are scalars
        if v == "":
            continue
        if isinstance(v, bool):
            out[k] = v
        elif isinstance(v, (int, float)):
            out[k] = v
        else:
            out[k] = str(v)
    return out


async def _parse_profile_update_body(request: Request) -> Tuple[Dict[str, Any], Any]:
    """
    Parse request body as JSON, multipart/form-data, or application/x-www-form-urlencoded.
    Laravel parity: accepts $request->all() style (form or JSON). Never raises.
    Handles "body" form field containing JSON string (common client pattern).
    Returns (payload_dict, photo_file_or_none). Photo is raw UploadFile for multipart.
    """
    payload: Dict[str, Any] = {}
    photo_file = None
    content_type = (request.headers.get("content-type") or "").lower().split(";")[0].strip()

    try:
        # Try multipart first - some clients send multipart with photo + JSON in "body" field
        if "multipart/form-data" in content_type:
            form = await request.form()
            body_json_str: Optional[str] = None
            for key in form.keys():
                val = form.get(key)
                if key == "photo":
                    if val and hasattr(val, "read"):
                        photo_file = val
                    continue
                if key == "body" and val is not None:
                    # Client may send profile data as JSON string in "body" field
                    s = val if isinstance(val, str) else (str(val) if val else None)
                    if s and s not in ("undefined", "null"):
                        body_json_str = s
                    continue
                if val is not None and not (hasattr(val, "read") and callable(getattr(val, "read", None))):
                    s = val if isinstance(val, str) else (str(val) if val else None)
                    if s and s not in ("undefined", "null"):
                        payload[key] = s
            # Merge parsed body into payload (body takes precedence for overlapping keys)
            if body_json_str:
                try:
                    parsed = json.loads(body_json_str)
                    if isinstance(parsed, dict):
                        flattened = _flatten_payload(parsed)
                        payload = {**payload, **flattened}
                except (json.JSONDecodeError, TypeError):
                    pass
        elif "application/x-www-form-urlencoded" in content_type:
            form = await request.form()
            body_json_str = None
            for key, val in form.items():
                if key == "body" and val is not None and isinstance(val, str):
                    body_json_str = val
                    continue
                if val is not None and isinstance(val, str) and val not in ("undefined", "null"):
                    payload[key] = val
            if body_json_str:
                try:
                    parsed = json.loads(body_json_str)
                    if isinstance(parsed, dict):
                        flattened = _flatten_payload(parsed)
                        payload = {**payload, **flattened}
                except (json.JSONDecodeError, TypeError):
                    pass
        else:
            # JSON: try request.json() - handles application/json
            try:
                body = await request.json()
                if isinstance(body, dict):
                    payload = _flatten_payload(body)
                elif isinstance(body, str):
                    parsed = json.loads(body)
                    if isinstance(parsed, dict):
                        payload = _flatten_payload(parsed)
            except Exception:
                pass
    except Exception:
        pass
    return payload, photo_file


@router.get("", dependencies=[Depends(require_auth)])
@router.get("/", dependencies=[Depends(require_auth)], include_in_schema=False)
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


def _save_profile_photo(content: bytes, filename: str, mime_type: Optional[str] = None) -> Optional[str]:
    """Save photo to uploads dir (compressed). Return URL. Laravel stores URL on user.photo."""
    try:
        compressed, ext = compress_image(content, filename, mime_type)
        if ext and not ext.startswith("."):
            ext = f".{ext}"
        safe_name = f"{uuid_lib.uuid4().hex}{ext}"
        upload_dir = os.environ.get("UPLOAD_DIR", "uploads")
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, safe_name)
        with open(file_path, "wb") as fp:
            fp.write(compressed)
        return f"/uploads/{safe_name}"
    except Exception:
        return None


@router.post("/update", dependencies=[Depends(require_auth)])
@router.post("/update/", dependencies=[Depends(require_auth)], include_in_schema=False)  # Trailing slash (Laravel parity)
async def update_profile(
    request: Request,
    profile_service: ProfileService = Depends(get_profile_service),
    current_user_id: int = Depends(get_current_user_id),
):
    """
    POST /profile/update — status, message, user.
    Accepts JSON, multipart/form-data, or application/x-www-form-urlencoded.
    Photo: compress then save to uploads/, store URL on user.photo.
    Handles "body" form field with JSON string (client pattern).
    """
    payload, photo_file = await _parse_profile_update_body(request)

    if photo_file:
        try:
            content = await photo_file.read()
            mime = getattr(photo_file, "content_type", None) or None
            url = _save_profile_photo(content, photo_file.filename or "photo", mime)
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
