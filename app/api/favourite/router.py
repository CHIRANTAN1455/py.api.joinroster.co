from fastapi import APIRouter, Depends

from app.core.dependencies import require_auth


router = APIRouter(prefix="/favourite", tags=["favourite"])


@router.get("", dependencies=[Depends(require_auth)])
def list_favourites():
    return {"status": "success"}


@router.post("", dependencies=[Depends(require_auth)])
def create_favourite():
    return {"status": "success"}

