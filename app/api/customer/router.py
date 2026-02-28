from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user_id, require_auth, unlimited_rate
from app.core.laravel_response import success_with_message
from app.db.session import get_db
from app.services.customer_service import CustomerService


router = APIRouter(prefix="/customer", tags=["customer"])


def get_customer_service(db: Session = Depends(get_db)) -> CustomerService:
    return CustomerService(db=db)


@router.post("/register", dependencies=[Depends(require_auth)])
def customer_register(
    service: CustomerService = Depends(get_customer_service),
    current_user_id: int = Depends(get_current_user_id),
):
    customer = service.register(current_user_id, None)
    return success_with_message("Customer registered", customer=customer or {}, creators=[])


@router.post("/sendgrid/webhook", dependencies=[Depends(unlimited_rate)])
def customer_sendgrid_webhook():
    return success_with_message("Success")


@router.get("/by-user", dependencies=[Depends(require_auth)])
def customer_by_user(
    service: CustomerService = Depends(get_customer_service),
    current_user_id: int = Depends(get_current_user_id),
):
    customer = service.get_by_user(current_user_id)
    return success_with_message("Customer Loaded Successfully", customer=customer or {})


@router.post("/upgrade", dependencies=[Depends(require_auth)])
def customer_upgrade(
    service: CustomerService = Depends(get_customer_service),
    current_user_id: int = Depends(get_current_user_id),
):
    customer = service.upgrade(current_user_id, None)
    return success_with_message("Customer Loaded Successfully", customer=customer or {})


@router.get("/billing", dependencies=[Depends(require_auth)])
def customer_billing(
    service: CustomerService = Depends(get_customer_service),
    current_user_id: int = Depends(get_current_user_id),
):
    customer = service.get_by_user(current_user_id)
    return success_with_message("Billing Loaded Successfully", billing=customer or {})
