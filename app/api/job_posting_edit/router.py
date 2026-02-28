from fastapi import APIRouter, Depends

from app.core.dependencies import require_auth
from app.core.laravel_response import success_with_message


router = APIRouter(prefix="/job-posting", tags=["job-posting-edit"])


@router.patch("/edit/{uuid}", dependencies=[Depends(require_auth)])
def job_posting_edit(uuid: str):
    return success_with_message("Job posting updated", project={})
