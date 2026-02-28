from fastapi import APIRouter, Depends

from app.core.dependencies import require_auth, unlimited_rate


router = APIRouter(prefix="/user", tags=["user"])


@router.post(
    "/{id}/slack",
    dependencies=[Depends(require_auth), Depends(unlimited_rate)],
)
def user_slack(id: int):
    """
    POST /user/{id}/slack
    Middleware: auth:sanctum, api.unlimited
    """
    return {"status": "success", "id": id}


@router.patch("/{id}", dependencies=[Depends(require_auth)])
def update_user(id: int):
    """
    PATCH /user/{id}
    Middleware: auth:sanctum
    """
    return {"status": "success", "id": id}


@router.patch("/{id}/timezone", dependencies=[Depends(require_auth)])
def update_user_timezone(id: int):
    """
    PATCH /user/{id}/timezone
    Middleware: auth:sanctum
    """
    return {"status": "success", "id": id}


@router.post("/{id}/jobtypes", dependencies=[Depends(require_auth)])
def update_user_jobtypes(id: int):
    """
    POST /user/{id}/jobtypes
    Middleware: auth:sanctum
    """
    return {"status": "success", "id": id}


@router.post("/{id}/content-vertical", dependencies=[Depends(require_auth)])
def update_user_content_vertical(id: int):
    """
    POST /user/{id}/content-vertical
    Middleware: auth:sanctum
    """
    return {"status": "success", "id": id}


@router.post("/{id}/platforms", dependencies=[Depends(require_auth)])
def update_user_platforms(id: int):
    """
    POST /user/{id}/platforms
    Middleware: auth:sanctum
    """
    return {"status": "success", "id": id}


@router.post("/{id}/revert-update-time", dependencies=[Depends(require_auth)])
def revert_user_update_time(id: int):
    """
    POST /user/{id}/revert-update-time
    Middleware: auth:sanctum
    """
    return {"status": "success", "id": id}


@router.post("/{id}/policy-acceptance", dependencies=[Depends(require_auth)])
def user_policy_acceptance(id: int):
    """
    POST /user/{id}/policy-acceptance
    Middleware: auth:sanctum
    """
    return {"status": "success", "id": id}


@router.delete("/{id}", dependencies=[Depends(require_auth)])
def delete_user(id: int):
    """
    DELETE /user/{id}
    Middleware: auth:sanctum
    """
    return {"status": "success", "id": id}


@router.get("/referral/{code}")
def user_referral(code: str):
    """
    GET /user/referral/{code}
    Middleware: none
    """
    return {"status": "success", "code": code}


@router.post("/notifications/{id}")
def user_notifications(id: int):
    """
    POST /user/notifications/{id}
    Middleware: none
    """
    return {"status": "success", "id": id}

