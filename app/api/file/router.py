from fastapi import APIRouter, Depends

from app.core.dependencies import require_auth
from app.core.laravel_response import success_with_message


router = APIRouter(prefix="/file", tags=["file"])


@router.post("", dependencies=[Depends(require_auth)])
def file_upload():
    return success_with_message("File uploaded", file={}, url=None)
