from fastapi import APIRouter, Depends

from app.core.dependencies import require_auth


router = APIRouter(prefix="/job-posting", tags=["job-posting-edit"])


@router.patch("/edit/{uuid}", dependencies=[Depends(require_auth)])
def job_posting_edit(uuid: str):
    return {"status": "success", "uuid": uuid}

