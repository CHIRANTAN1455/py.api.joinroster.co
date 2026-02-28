from fastapi import APIRouter, Depends

from app.core.dependencies import require_auth


router = APIRouter(prefix="/profile-visit", tags=["profile-visit"])


@router.post("", dependencies=[Depends(require_auth)])
def profile_visit():
    return {"status": "success"}

