"""
Laravel-compatible request/response schemas for public endpoints.
Use these so Swagger shows the same payload shape as the Laravel API.
"""
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


# ——— /api/pdfsend (PATCH) ———
class PdfSendBody(BaseModel):
    """Laravel PdfSend: typical payload for PDF send (email, type, pdf_link, etc.)."""
    email: Optional[str] = Field(None, description="Recipient email")
    type: Optional[str] = Field(None, description="PDF type / template")
    user_id: Optional[int] = Field(None, description="User ID")
    name: Optional[str] = Field(None, description="Recipient name")
    pdf_link: Optional[str] = Field(None, description="URL of PDF to attach to the email")
    fol_count: Optional[str] = Field(None, description="Follower count band (e.g. 0-10k)")

    class Config:
        extra = "allow"  # Accept any extra keys from Laravel payload
        json_schema_extra = {
            "example": {"email": "user@example.com", "type": "invoice", "pdf_link": "https://example.com/guide.pdf"}
        }


class PdfSendResponse(BaseModel):
    """Laravel response: status, message."""
    status: str = "success"
    message: str = "Success"


# ——— /api/freejobpost (PATCH) ———
class FreeJobPostBody(BaseModel):
    """Laravel FreeJobPostingController: claim free job post (e.g. from referral)."""
    user_id: Optional[int] = None
    referral_code: Optional[str] = None

    class Config:
        extra = "allow"
        json_schema_extra = {"example": {"user_id": 1}}


class FreeJobPostResponse(BaseModel):
    status: str = "success"
    message: str = "Success"


# ——— Callbacks (accept raw body for webhooks) ———
class CallbackStripeBody(BaseModel):
    """Stripe webhook payload (simplified for docs)."""
    type: Optional[str] = None
    data: Optional[Dict[str, Any]] = None


class CallbackWebflowBody(BaseModel):
    """Webflow callback payload."""
    payload: Optional[Dict[str, Any]] = None
