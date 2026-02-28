"""Payment. Path {id} = uuid. Laravel-exact: status, message, payment/payments."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user_id, require_auth
from app.core.laravel_response import success_with_message
from app.db.session import get_db
from app.services.payment_service import PaymentService


router = APIRouter(prefix="/payment", tags=["payment"])


def get_payment_service(db: Session = Depends(get_db)) -> PaymentService:
    return PaymentService(db=db)


@router.get("", dependencies=[Depends(require_auth)])
def list_payments(
    service: PaymentService = Depends(get_payment_service),
    current_user_id: int = Depends(get_current_user_id),
):
    payments = service.list(current_user_id)
    return success_with_message("Payments Loaded Successfully", payments=payments)


@router.post("", dependencies=[Depends(require_auth)])
def create_payment(
    body: dict = None,
    service: PaymentService = Depends(get_payment_service),
    current_user_id: int = Depends(get_current_user_id),
):
    payment = service.create(current_user_id, body or {})
    return success_with_message("Payment Created Successfully", payment=payment or {})


@router.delete("/{id}", dependencies=[Depends(require_auth)])
def delete_payment(
    id: str,
    service: PaymentService = Depends(get_payment_service),
    current_user_id: int = Depends(get_current_user_id),
):
    ok = service.delete(id, current_user_id)
    if not ok:
        return {"status": "error", "message": "Payment not found"}
    return success_with_message("Payment Deleted Successfully")
