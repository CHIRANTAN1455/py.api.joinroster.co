from fastapi import APIRouter, Depends

from app.core.dependencies import require_auth
from app.core.laravel_response import success_with_message


router = APIRouter(prefix="/profile-visit", tags=["profile-visit"])


@router.post("", dependencies=[Depends(require_auth)])
def profile_visit():
    return success_with_message("Profile visit recorded")
