"""Payment. Path {id} = uuid. Laravel-exact: status, message, payment/payments."""
from fastapi import APIRouter, Depends

from app.core.dependencies import require_auth
from app.core.laravel_response import success_with_message


router = APIRouter(prefix="/payment", tags=["payment"])


@router.get("", dependencies=[Depends(require_auth)])
def list_payments():
    return success_with_message("Payments Loaded Successfully", payments=[])


@router.post("", dependencies=[Depends(require_auth)])
def create_payment():
    return success_with_message("Payment Created Successfully", payment={})


@router.delete("/{id}", dependencies=[Depends(require_auth)])
def delete_payment(id: str):
    return success_with_message("Payment Deleted Successfully")
