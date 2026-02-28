"""Public/callback endpoints. Laravel-exact: status, message where applicable."""
from fastapi import APIRouter, Depends

from app.core.dependencies import unlimited_rate
from app.core.laravel_response import success_with_message


router = APIRouter(prefix="", tags=["public"])


@router.post(
    "/callback/stripe",
    dependencies=[Depends(unlimited_rate)],
)
def callback_stripe():
    return success_with_message("Success")


@router.post(
    "/callback/post-transaction/slack",
    dependencies=[Depends(unlimited_rate)],
)
def callback_post_transaction_slack():
    return success_with_message("Success")


@router.post(
    "/callback/post-transaction/email",
    dependencies=[Depends(unlimited_rate)],
)
def callback_post_transaction_email():
    return success_with_message("Success")


@router.post(
    "/callback/webflow",
    dependencies=[Depends(unlimited_rate)],
)
def callback_webflow():
    return success_with_message("Success")


@router.post("/upload")
def upload_file():
    return success_with_message("File uploaded", file={}, url=None)


@router.post("/upload/multiple")
def upload_multiple_files():
    return success_with_message("Files uploaded", files=[])


@router.get("users/metrics")
def users_metrics():
    return success_with_message("Metrics loaded", metrics={})


@router.patch("/pdfsend")
def pdfsend():
    return success_with_message("Success")


@router.get("/public-job-listing")
def public_job_listing():
    return success_with_message("Job listings loaded", jobs=[], total=0, page=1)


@router.patch("/freejobpost")
def free_job_post():
    return success_with_message("Success")

