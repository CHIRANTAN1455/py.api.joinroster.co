from fastapi import APIRouter, Depends

from app.core.dependencies import require_auth
from app.core.laravel_response import success_with_message


router = APIRouter(prefix="/referral", tags=["referral"])


@router.get("/referral-records", dependencies=[Depends(require_auth)])
def referral_records():
    """Laravel: status, message, referrals."""
    return success_with_message("Referral Codes Loaded Successfully", referrals=[])


@router.get("/referral-paid-records", dependencies=[Depends(require_auth)])
def referral_paid_records():
    """Laravel: status, message, referrals, has_free_job_post_from_referral, eligible_for_free_job_post_from_referral."""
    return success_with_message(
        "Referral Codes Loaded Successfully",
        referrals=[],
        has_free_job_post_from_referral=False,
        eligible_for_free_job_post_from_referral=False,
    )

