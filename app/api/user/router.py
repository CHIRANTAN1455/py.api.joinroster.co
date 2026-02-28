"""User endpoints. Laravel-exact: status, message, user. Path {id} = user uuid."""
from fastapi import APIRouter, Depends

from app.core.dependencies import require_auth, unlimited_rate
from app.core.laravel_response import success_with_message


router = APIRouter(prefix="/user", tags=["user"])


@router.post("/{id}/slack", dependencies=[Depends(require_auth), Depends(unlimited_rate)])
def user_slack(id: str):
    return success_with_message("Success")


@router.patch("/{id}", dependencies=[Depends(require_auth)])
def update_user(id: str):
    return success_with_message("User Updated Successfully", user={})


@router.patch("/{id}/timezone", dependencies=[Depends(require_auth)])
def update_user_timezone(id: str):
    return success_with_message("User Updated Successfully", user={})


@router.post("/{id}/jobtypes", dependencies=[Depends(require_auth)])
def update_user_jobtypes(id: str):
    return success_with_message("Job Types Updated Successfully", user={})


@router.post("/{id}/content-vertical", dependencies=[Depends(require_auth)])
def update_user_content_vertical(id: str):
    return success_with_message("Content Verticals Updated Successfully", user={})


@router.post("/{id}/platforms", dependencies=[Depends(require_auth)])
def update_user_platforms(id: str):
    return success_with_message("Platforms Updated Successfully", user={})


@router.post("/{id}/revert-update-time", dependencies=[Depends(require_auth)])
def revert_user_update_time(id: str):
    return success_with_message("User Updated Successfully", user={})


@router.post("/{id}/policy-acceptance", dependencies=[Depends(require_auth)])
def user_policy_acceptance(id: str):
    return success_with_message("Policy accepted", user={})


@router.delete("/{id}", dependencies=[Depends(require_auth)])
def delete_user(id: str):
    return success_with_message("User Deleted Successfully")


@router.get("/referral/{code}")
def user_referral(code: str):
    return success_with_message("Referral Loaded Successfully", referral={}, valid=True)


@router.post("/notifications/{id}")
def user_notifications(id: str):
    return success_with_message("Success")
