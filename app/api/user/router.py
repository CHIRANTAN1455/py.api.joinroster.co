"""User endpoints. Laravel-exact: status, message, user. Path {id} = user uuid."""
from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.user.schemas import (
    UserContentVerticalBody,
    UserJobTypesBody,
    UserPlatformsBody,
    UserTimezoneBody,
    UserUpdateBody,
)
from app.core.dependencies import get_current_user_id, require_auth, unlimited_rate
from app.core.laravel_response import success_with_message, user_to_laravel_user_resource
from app.db.session import get_db
from app.services.user_service import UserService


router = APIRouter(prefix="/user", tags=["user"])


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db=db)


@router.post("/{id}/slack", dependencies=[Depends(require_auth), Depends(unlimited_rate)])
def user_slack(id: str):
    return success_with_message("Success")


@router.patch("/{id}", dependencies=[Depends(require_auth)])
def update_user(
    id: str,
    body: Optional[UserUpdateBody] = None,
    service: UserService = Depends(get_user_service),
    current_user_id: int = Depends(get_current_user_id),
):
    payload = body.model_dump(exclude_unset=True) if body else None
    user = service.update_by_uuid(id, current_user_id, payload)
    if not user:
        return {"status": "error", "message": "User not found", "user": {}}
    return success_with_message("User Updated Successfully", user=user_to_laravel_user_resource(user))


@router.patch("/{id}/timezone", dependencies=[Depends(require_auth)])
def update_user_timezone(
    id: str,
    body: Optional[UserTimezoneBody] = None,
    service: UserService = Depends(get_user_service),
    current_user_id: int = Depends(get_current_user_id),
):
    payload = body.model_dump(exclude_unset=True) if body else {}
    user = service.update_timezone(
        id, current_user_id,
        timezone=payload.get("timezone"),
        utc_offset=payload.get("utc_offset"),
    )
    if not user:
        return {"status": "error", "message": "User not found", "user": {}}
    return success_with_message("User Updated Successfully", user=user_to_laravel_user_resource(user))


@router.post("/{id}/jobtypes", dependencies=[Depends(require_auth)])
def update_user_jobtypes(
    id: str,
    body: Optional[UserJobTypesBody] = None,
    service: UserService = Depends(get_user_service),
    current_user_id: int = Depends(get_current_user_id),
):
    user = service.get_by_uuid(id)
    if not user or user.id != current_user_id:
        return {"status": "error", "message": "User not found", "user": {}}
    return success_with_message("Job Types Updated Successfully", user=user_to_laravel_user_resource(user))


@router.post("/{id}/content-vertical", dependencies=[Depends(require_auth)])
def update_user_content_vertical(
    id: str,
    body: Optional[UserContentVerticalBody] = None,
    service: UserService = Depends(get_user_service),
    current_user_id: int = Depends(get_current_user_id),
):
    user = service.get_by_uuid(id)
    if not user or user.id != current_user_id:
        return {"status": "error", "message": "User not found", "user": {}}
    return success_with_message("Content Verticals Updated Successfully", user=user_to_laravel_user_resource(user))


@router.post("/{id}/platforms", dependencies=[Depends(require_auth)])
def update_user_platforms(
    id: str,
    body: Optional[UserPlatformsBody] = None,
    service: UserService = Depends(get_user_service),
    current_user_id: int = Depends(get_current_user_id),
):
    user = service.get_by_uuid(id)
    if not user or user.id != current_user_id:
        return {"status": "error", "message": "User not found", "user": {}}
    return success_with_message("Platforms Updated Successfully", user=user_to_laravel_user_resource(user))


@router.post("/{id}/revert-update-time", dependencies=[Depends(require_auth)])
def revert_user_update_time(
    id: str,
    service: UserService = Depends(get_user_service),
    current_user_id: int = Depends(get_current_user_id),
):
    user = service.get_by_uuid(id)
    if not user or user.id != current_user_id:
        return {"status": "error", "message": "User not found", "user": {}}
    return success_with_message("User Updated Successfully", user=user_to_laravel_user_resource(user))


@router.post("/{id}/policy-acceptance", dependencies=[Depends(require_auth)])
def user_policy_acceptance(
    id: str,
    service: UserService = Depends(get_user_service),
    current_user_id: int = Depends(get_current_user_id),
):
    user = service.accept_policy(id, current_user_id)
    if not user:
        return {"status": "error", "message": "User not found", "user": {}}
    return success_with_message("Policy accepted", user=user_to_laravel_user_resource(user))


@router.delete("/{id}", dependencies=[Depends(require_auth)])
def delete_user(
    id: str,
    service: UserService = Depends(get_user_service),
    current_user_id: int = Depends(get_current_user_id),
):
    ok = service.delete_by_uuid(id, current_user_id)
    if not ok:
        return {"status": "error", "message": "User not found"}
    return success_with_message("User Deleted Successfully")


@router.get("/referral/{code}")
def user_referral(code: str, service: UserService = Depends(get_user_service)):
    result = service.get_referral_by_code(code)
    return success_with_message(
        "Referral Loaded Successfully",
        referral=result.get("referral", {}),
        valid=result.get("valid", False),
    )


@router.post("/notifications/{id}")
def user_notifications(
    id: str,
    service: UserService = Depends(get_user_service),
    current_user_id: int = Depends(get_current_user_id),
):
    return success_with_message("Success")
