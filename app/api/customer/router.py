from fastapi import APIRouter, Depends

from app.core.dependencies import unlimited_rate


router = APIRouter(prefix="/customer", tags=["customer"])


@router.post("/register")
def customer_register():
    """
    POST /customer/register
    Middleware: none
    """
    return {"status": "success"}


@router.post(
    "/sendgrid/webhook",
    dependencies=[Depends(unlimited_rate)],
)
def customer_sendgrid_webhook():
    """
    POST /customer/sendgrid/webhook
    Middleware: api.unlimited
    """
    return {"status": "success"}


@router.get("/by-user")
def customer_by_user():
    """
    GET /customer/by-user
    Middleware: none
    """
    return {"status": "success"}


@router.post("/upgrade")
def customer_upgrade():
    """
    POST /customer/upgrade
    Middleware: none
    """
    return {"status": "success"}


@router.get("/billing")
def customer_billing():
    """
    GET /customer/billing
    Middleware: none
    """
    return {"status": "success"}

