from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user_id, require_auth
from app.core.laravel_response import success_with_message
from app.db.session import get_db
from app.services.file_service import FileService


router = APIRouter(prefix="/file", tags=["file"])


def get_file_service(db: Session = Depends(get_db)) -> FileService:
    return FileService(db=db)


@router.post("", dependencies=[Depends(require_auth)])
def file_upload(
    file: UploadFile = File(...),
    service: FileService = Depends(get_file_service),
    current_user_id: int = Depends(get_current_user_id),
):
    content = file.file.read()
    result = service.create(current_user_id, file.filename or "upload", content=content)
    if not result:
        return success_with_message("File uploaded", file={}, url=None)
    return success_with_message("File uploaded", file=result, url=result.get("url"))
