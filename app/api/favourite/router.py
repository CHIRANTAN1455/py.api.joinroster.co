from fastapi import APIRouter, Depends

from app.core.dependencies import require_auth
from app.core.laravel_response import success_with_message


router = APIRouter(prefix="/favourite", tags=["favourite"])


@router.get("", dependencies=[Depends(require_auth)])
def list_favourites():
    return success_with_message("Favourites Loaded Successfully", favourites=[])


@router.post("", dependencies=[Depends(require_auth)])
def create_favourite():
    return success_with_message("Favourite Created Successfully", favourite={})
