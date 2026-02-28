from fastapi import APIRouter, Depends

from app.core.dependencies import unlimited_rate
from app.core.laravel_response import success_with_message


router = APIRouter(prefix="/customer", tags=["customer"])


@router.post("/register")
def customer_register():
    return success_with_message("Customer registered", customer={}, creators=[])


@router.post("/sendgrid/webhook", dependencies=[Depends(unlimited_rate)])
def customer_sendgrid_webhook():
    return success_with_message("Success")


@router.get("/by-user")
def customer_by_user():
    return success_with_message("Customer Loaded Successfully", customer={})


@router.post("/upgrade")
def customer_upgrade():
    return success_with_message("Customer Loaded Successfully", customer={})


@router.get("/billing")
def customer_billing():
    return success_with_message("Billing Loaded Successfully", billing={})
