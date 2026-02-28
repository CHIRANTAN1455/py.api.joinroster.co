from fastapi import APIRouter, Depends

from app.core.dependencies import unlimited_rate


router = APIRouter(prefix="", tags=["public"])


@router.post(
    "/callback/stripe",
    dependencies=[Depends(unlimited_rate)],
)
def callback_stripe():
    """
    POST /callback/stripe
    Middleware: api.unlimited
    """
    return {"status": "success"}


@router.post(
    "/callback/post-transaction/slack",
    dependencies=[Depends(unlimited_rate)],
)
def callback_post_transaction_slack():
    """
    POST /callback/post-transaction/slack
    Middleware: api.unlimited
    """
    return {"status": "success"}


@router.post(
    "/callback/post-transaction/email",
    dependencies=[Depends(unlimited_rate)],
)
def callback_post_transaction_email():
    """
    POST /callback/post-transaction/email
    Middleware: api.unlimited
    """
    return {"status": "success"}


@router.post(
    "/callback/webflow",
    dependencies=[Depends(unlimited_rate)],
)
def callback_webflow():
    """
    POST /callback/webflow
    Middleware: api.unlimited
    """
    return {"status": "success"}


@router.post("/upload")
def upload_file():
    """
    POST /upload
    Middleware: none
    """
    return {"status": "success"}


@router.post("/upload/multiple")
def upload_multiple_files():
    """
    POST /upload/multiple
    Middleware: none
    """
    return {"status": "success"}


@router.get("users/metrics")
def users_metrics():
    """
    GET users/metrics
    Middleware: none
    NOTE: Path is exactly as in spec (no leading slash).
    """
    return {"status": "success"}


@router.patch("/pdfsend")
def pdfsend():
    """
    PATCH /pdfsend
    Middleware: none
    """
    return {"status": "success"}


@router.get("/public-job-listing")
def public_job_listing():
    """
    GET /public-job-listing
    Middleware: none
    """
    return {"status": "success"}


@router.patch("/freejobpost")
def free_job_post():
    """
    PATCH /freejobpost
    Middleware: none
    """
    return {"status": "success"}

