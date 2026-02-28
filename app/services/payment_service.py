"""Payment CRUD."""
import uuid as uuid_lib
from datetime import datetime
from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

from app.db.models.payment import Payment


def _payment_resource(p: Payment) -> Dict[str, Any]:
    return {"uuid": p.uuid, "amount": float(p.amount) if p.amount else None, "status": p.status, "created_at": p.created_at}


class PaymentService:
    def __init__(self, db: Session):
        self.db = db

    def list(self, user_id: int) -> List[Dict[str, Any]]:
        try:
            items = self.db.query(Payment).filter(Payment.user_id == user_id).order_by(Payment.created_at.desc()).all()
            return [_payment_resource(p) for p in items]
        except Exception:
            return []

    def create(self, user_id: int, payload: Any) -> Optional[Dict[str, Any]]:
        try:
            amount = payload.get("amount") if isinstance(payload, dict) else getattr(payload, "amount", None)
            status = payload.get("status", "pending") if isinstance(payload, dict) else getattr(payload, "status", "pending")
            p = Payment(uuid=str(uuid_lib.uuid4()), user_id=user_id, amount=amount, status=status, created_at=datetime.utcnow(), updated_at=datetime.utcnow())
            self.db.add(p)
            self.db.commit()
            self.db.refresh(p)
            return _payment_resource(p)
        except Exception:
            return None

    def delete(self, uuid: str, user_id: int) -> bool:
        try:
            p = self.db.query(Payment).filter(Payment.uuid == uuid, Payment.user_id == user_id).first()
            if not p:
                return False
            self.db.delete(p)
            self.db.commit()
            return True
        except Exception:
            return False
