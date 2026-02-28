"""
Referral records service: list referral records and paid records for current user.
Laravel parity for /referral-records and /referral-paid-records.
"""
from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

from app.db.models.referral_record import ReferralRecord
from app.db.models.user import User


def _referral_record_to_resource(record: ReferralRecord, referred_user: Optional[User]) -> Dict[str, Any]:
    """Laravel referral record resource shape (uuid, code, referred user, etc.)."""
    return {
        "uuid": getattr(record, "uuid", None),
        "code": getattr(record, "code", None),
        "paid": bool(getattr(record, "paid", 0)),
        "created_at": getattr(record, "created_at", None),
        "referred_user": {
            "uuid": referred_user.uuid if referred_user else None,
            "name": referred_user.name if referred_user else None,
            "email": referred_user.email if referred_user else None,
        } if referred_user else None,
    }


class ReferralService:
    def __init__(self, db: Session):
        self.db = db

    def get_records(self, user_id: int) -> List[Dict[str, Any]]:
        """All referral records where current user is the referrer."""
        try:
            rows = (
                self.db.query(ReferralRecord)
                .filter(ReferralRecord.referrer_user_id == user_id)
                .order_by(ReferralRecord.created_at.desc())
                .all()
            )
            out = []
            for r in rows:
                referred = self.db.query(User).filter(User.id == r.referred_user_id).first()
                out.append(_referral_record_to_resource(r, referred))
            return out
        except Exception:
            return []

    def get_paid_records(self, user_id: int) -> List[Dict[str, Any]]:
        """Referral records where reward was paid."""
        try:
            rows = (
                self.db.query(ReferralRecord)
                .filter(
                    ReferralRecord.referrer_user_id == user_id,
                    ReferralRecord.paid == 1,
                )
                .order_by(ReferralRecord.created_at.desc())
                .all()
            )
            out = []
            for r in rows:
                referred = self.db.query(User).filter(User.id == r.referred_user_id).first()
                out.append(_referral_record_to_resource(r, referred))
            return out
        except Exception:
            return []

    def has_free_job_post_from_referral(self, user_id: int) -> bool:
        """Whether user has a free job post from referral (e.g. first referral)."""
        try:
            count = (
                self.db.query(ReferralRecord)
                .filter(ReferralRecord.referrer_user_id == user_id)
                .count()
            )
            return count > 0
        except Exception:
            return False

    def eligible_for_free_job_post_from_referral(self, user_id: int) -> bool:
        """Whether user is eligible for a free job post (e.g. has referrals not yet claimed)."""
        try:
            paid_count = (
                self.db.query(ReferralRecord)
                .filter(
                    ReferralRecord.referrer_user_id == user_id,
                    ReferralRecord.paid == 1,
                )
                .count()
            )
            total = (
                self.db.query(ReferralRecord)
                .filter(ReferralRecord.referrer_user_id == user_id)
                .count()
            )
            return total > paid_count
        except Exception:
            return False
