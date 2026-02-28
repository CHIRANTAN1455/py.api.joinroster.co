from fastapi import APIRouter, Depends

from app.core.dependencies import require_auth


router = APIRouter(prefix="/referral", tags=["referral"])


@router.get("/referral-records", dependencies=[Depends(require_auth)])
def referral_records():
    return {"status": "success"}


@router.get("/referral-paid-records", dependencies=[Depends(require_auth)])
def referral_paid_records():
    return {"status": "success"}

