"""Public/callback endpoints. Laravel-exact: status, message where applicable."""
from typing import Optional

from fastapi import APIRouter, Body, Depends, File, Query, UploadFile
from sqlalchemy.orm import Session

from app.api.public.schemas import FreeJobPostBody, PdfSendBody
from app.core.dependencies import unlimited_rate
from app.core.laravel_response import success_with_message
from app.db.session import get_db
from app.db.models.user import User
from app.services.email_service import send_pdf_email
from app.services.file_service import FileService
from app.services.matching_service import MatchingService
from app.services.project_service import ProjectService


router = APIRouter(prefix="", tags=["public"])


def get_db_session(db: Session = Depends(get_db)):
    return db


@router.post("/callback/stripe", dependencies=[Depends(unlimited_rate)])
def callback_stripe():
    return success_with_message("Success")


@router.post("/callback/post-transaction/slack", dependencies=[Depends(unlimited_rate)])
def callback_post_transaction_slack():
    return success_with_message("Success")


@router.post("/callback/post-transaction/email", dependencies=[Depends(unlimited_rate)])
def callback_post_transaction_email():
    return success_with_message("Success")


@router.post("/callback/webflow", dependencies=[Depends(unlimited_rate)])
def callback_webflow():
    return success_with_message("Success")


@router.post("/upload")
def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db_session),
):
    content = file.file.read()
    service = FileService(db)
    result = service.create(0, file.filename or "upload", content=content)
    if not result:
        return success_with_message("File uploaded", file={}, url=None)
    return success_with_message("File uploaded", file=result, url=result.get("url"))


@router.post("/upload/multiple")
def upload_multiple_files(
    files: list[UploadFile] = File(...),
    db: Session = Depends(get_db_session),
):
    service = FileService(db)
    out = []
    for f in files:
        content = f.file.read()
        r = service.create(0, f.filename or "upload", content=content)
        if r:
            out.append(r)
    return success_with_message("Files uploaded", files=out)


@router.get("users/metrics")
def users_metrics(db: Session = Depends(get_db_session)):
    return success_with_message("Metrics loaded", metrics={"users": 0})


@router.patch(
    "/pdfsend",
    response_model=None,
    responses={
        200: {
            "description": "Laravel-compatible response",
            "content": {
                "application/json": {
                    "example": {"status": "success", "message": "Success"}
                }
            },
        }
    },
)
def pdfsend(
    body: Optional[PdfSendBody] = Body(None, description="Laravel PdfSend payload"),
    db: Session = Depends(get_db_session),
):
    """Send PDF/document email to the given email (or user_id). Requires body with email or user_id."""
    email = None
    name = None
    pdf_type = None
    if body:
        email = body.email
        name = body.name
        pdf_type = body.type
        if not email and body.user_id:
            user = db.query(User).filter(User.id == body.user_id).first()
            if user:
                email = user.email
                if not name and user.name:
                    name = user.name
    if not email or "@" not in email:
        return {"status": "error", "message": "Valid email or user_id is required"}
    ok, err = send_pdf_email(to_email=email, pdf_type=pdf_type, recipient_name=name)
    if not ok:
        return {"status": "error", "message": err or "Failed to send email"}
    return success_with_message("Success")


@router.get("/public-job-listing")
def public_job_listing(
    page: int = Query(1, ge=1),
    db: Session = Depends(get_db_session),
):
    service = ProjectService(db)
    result = service.public_search_no_auth(page=page)
    return success_with_message("Job listings loaded", jobs=result["projects"], total=result["total"], page=result["page"])


@router.patch(
    "/freejobpost",
    response_model=None,
    responses={
        200: {
            "description": "Laravel-compatible response",
            "content": {
                "application/json": {
                    "example": {"status": "success", "message": "Success"}
                }
            },
        }
    },
)
def free_job_post(body: Optional[FreeJobPostBody] = Body(None, description="Laravel FreeJobPost payload")):
    """Accept same payload as Laravel FreeJobPostingController (user_id, referral_code)."""
    return success_with_message("Success")


@router.post("/public-matching")
def public_matching(db: Session = Depends(get_db_session)):
    service = MatchingService(db)
    data = service.create(0, None, None)
    if not data:
        return success_with_message("Matching created", matching={}, token=None)
    return success_with_message("Matching created", matching=data, token=data.get("token"))

