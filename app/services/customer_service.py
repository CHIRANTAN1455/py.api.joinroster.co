"""Customer (billing) CRUD."""
import uuid as uuid_lib
from datetime import datetime
from typing import Any, Dict, Optional

from sqlalchemy.orm import Session

from app.core.laravel_response import user_to_laravel_user_resource
from app.db.models.customer import Customer
from app.db.models.user import User


def _customer_resource(c: Customer, user: Optional[User] = None) -> Dict[str, Any]:
    out = {"uuid": c.uuid, "stripe_id": c.stripe_id, "created_at": c.created_at}
    if user:
        out["user"] = user_to_laravel_user_resource(user)
    return out


class CustomerService:
    def __init__(self, db: Session):
        self.db = db

    def get_by_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        try:
            c = self.db.query(Customer).filter(Customer.user_id == user_id).first()
            if not c:
                return None
            user = self.db.query(User).filter(User.id == c.user_id).first()
            return _customer_resource(c, user)
        except Exception:
            return None

    def register(self, user_id: int, payload: Any = None) -> Optional[Dict[str, Any]]:
        try:
            c = self.db.query(Customer).filter(Customer.user_id == user_id).first()
            if c:
                user = self.db.query(User).filter(User.id == c.user_id).first()
                return _customer_resource(c, user)
            stripe_id = payload.get("stripe_id", "") if isinstance(payload, dict) else getattr(payload, "stripe_id", "")
            c = Customer(uuid=str(uuid_lib.uuid4()), user_id=user_id, stripe_id=stripe_id, created_at=datetime.utcnow(), updated_at=datetime.utcnow())
            self.db.add(c)
            self.db.commit()
            self.db.refresh(c)
            user = self.db.query(User).filter(User.id == user_id).first()
            return _customer_resource(c, user)
        except Exception:
            return None

    def upgrade(self, user_id: int, payload: Any = None) -> Optional[Dict[str, Any]]:
        return self.get_by_user(user_id)
