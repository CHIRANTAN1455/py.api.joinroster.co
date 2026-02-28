"""Referral routes. Laravel paths are /referral-records and /referral-paid-records (no /referral/ prefix)."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user_id, require_auth
from app.core.laravel_response import success_with_message
from app.db.session import get_db
from app.services.referral_service import ReferralService


router = APIRouter(prefix="", tags=["referral"])


def get_referral_service(db: Session = Depends(get_db)) -> ReferralService:
    return ReferralService(db=db)


@router.get("/referral-records", dependencies=[Depends(require_auth)])
def referral_records(
    referral_service: ReferralService = Depends(get_referral_service),
    current_user_id: int = Depends(get_current_user_id),
):
    """Laravel: status, message, referrals (real data from referral_records table)."""
    referrals = referral_service.get_records(current_user_id)
    return success_with_message("Referral Codes Loaded Successfully", referrals=referrals)


@router.get("/referral-paid-records", dependencies=[Depends(require_auth)])
def referral_paid_records(
    referral_service: ReferralService = Depends(get_referral_service),
    current_user_id: int = Depends(get_current_user_id),
):
    """Laravel: status, message, referrals, has_free_job_post_from_referral, eligible_for_free_job_post_from_referral."""
    referrals = referral_service.get_paid_records(current_user_id)
    has_free = referral_service.has_free_job_post_from_referral(current_user_id)
    eligible = referral_service.eligible_for_free_job_post_from_referral(current_user_id)
    return success_with_message(
        "Referral Codes Loaded Successfully",
        referrals=referrals,
        has_free_job_post_from_referral=has_free,
        eligible_for_free_job_post_from_referral=eligible,
    )

