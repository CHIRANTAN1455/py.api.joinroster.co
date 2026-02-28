from fastapi import APIRouter, Depends

from app.core.dependencies import require_auth


router = APIRouter(prefix="/file", tags=["file"])


@router.post("", dependencies=[Depends(require_auth)])
def file_upload():
    return {"status": "success"}

