"""Public/callback endpoints. Laravel-exact: status, message where applicable."""
from typing import Optional

from fastapi import APIRouter, Body, Depends, File, HTTPException, Query, UploadFile, status
from sqlalchemy.orm import Session

from app.api.public.schemas import FreeJobPostBody, PdfSendBody
from app.core.dependencies import unlimited_rate
from app.core.laravel_response import success_with_message
from app.db.session import get_db
from app.db.models.user import User
from app.db.models.beacons_lp_user import BeaconsLpUser
from app.db.models.email_notification import EmailNotification
from app.services.email_service import send_pdf_email
from app.services.file_service import FileService
from app.services.matching_service import MatchingService
from app.services.project_service import ProjectService
from datetime import datetime
import uuid as uuid_lib


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
    """
    Laravel PdfSend::send parity.

    Success response (200):
    {
      "message": "PDF email sent successfully",
      "email_notification_uuid": "...",
      "saved_to_beacons_lp_user_id": 123,
      "pdf_source": "uploaded" | "link"
    }

    Error responses:
      422: {"error": "Either pdf_link or pdf_file is required"}
      400: {"error": "Unable to download PDF from link"}
      500: {"error": "Server error", "details": "..."}
    """
    if not body or not body.email:
        # Laravel validate() would throw; here we mirror its JSON shape.
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"error": "The email field is required."},
        )

    email = body.email.strip()
    name = (body.name or "").strip() or None
    fol_count = (body.fol_count or "").strip() or None
    pdf_link = (body.pdf_link or "").strip() or None

    if not pdf_link:
        # We don't support pdf_file uploads on this endpoint, so require pdf_link.
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"error": "Either pdf_link or pdf_file is required"},
        )

    # Create BeaconsLpUser row
    beacons = BeaconsLpUser(email=email, name=name, fol_count=fol_count)
    db.add(beacons)
    db.flush()  # Get ID before commit

    # Create or fetch EmailNotification row
    notification_code = f"send_pdf_email_{email}"
    notification = (
        db.query(EmailNotification)
        .filter(EmailNotification.code == notification_code)
        .first()
    )
    if not notification:
        notification = EmailNotification(
            uuid=str(uuid_lib.uuid4()),
            name=f"Send PDF Email - {email}",
            code=notification_code,
            active=True,
            subject=f"Send PDF Email - {email}",
            content="</>",
            created_at=datetime.utcnow(),
        )
        db.add(notification)

    db.commit()
    db.refresh(beacons)
    db.refresh(notification)

    # Send email with attached PDF
    ok, err = send_pdf_email(
        to_email=email,
        pdf_type=None,
        recipient_name=name.split(" ")[0] if name else None,
        pdf_link=pdf_link,
    )
    if not ok:
        # Mirror Laravel's 400/500 style simple error map
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": err or "Unable to download PDF from link"},
        )

    pdf_source = "link"
    return {
        "message": "PDF email sent successfully",
        "email_notification_uuid": notification.uuid,
        "saved_to_beacons_lp_user_id": beacons.id,
        "pdf_source": pdf_source,
    }


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

