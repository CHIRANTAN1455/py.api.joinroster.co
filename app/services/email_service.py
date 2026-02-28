"""
Email sending: SMTP (Laravel MAIL_*) or SendGrid API.
All copy from Laravel: app/core/email_copies.py (resources/views/emails/*.blade.php).
Supports attachments for all emails (PDF and other files).
"""
import base64
import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Any, List, Optional, Tuple

import requests

from app.core import email_copies

try:
    from sendgrid import SendGridAPIClient
    from sendgrid.helpers.mail import Mail, Email, To, Content, Attachment, FileContent, FileName, FileType
    SENDGRID_AVAILABLE = True
except ImportError:
    SENDGRID_AVAILABLE = False


# One attachment: (filename, raw_bytes, content_type)
AttachmentSpec = Tuple[str, bytes, str]


def fetch_url_as_bytes(url: str, timeout: int = 30) -> Tuple[Optional[bytes], Optional[str]]:
    """Fetch URL and return (content_bytes, error_message). Returns (None, msg) on failure."""
    try:
        r = requests.get(url, timeout=timeout)
        r.raise_for_status()
        return r.content, None
    except Exception as e:
        return None, str(e)


def get_from_email() -> str:
    addr = os.getenv("MAIL_FROM_ADDRESS") or os.getenv("SENDGRID_FROM_EMAIL")
    return addr.strip('"') if addr else "noreply@example.com"


def get_from_name() -> str:
    name = os.getenv("MAIL_FROM_NAME") or os.getenv("APP_NAME", "Roster")
    if not name:
        return "Roster"
    name = name.strip('"')
    if name == "${APP_NAME}":
        return os.getenv("APP_NAME", "Roster")
    return name


def _send_via_smtp(
    to_email: str,
    subject: str,
    plain_content: str,
    html_content: Optional[str],
    from_addr: str,
    from_name: str,
    attachments: Optional[List[AttachmentSpec]] = None,
) -> Tuple[bool, Optional[str]]:
    """Send using SMTP (MAIL_HOST, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD)."""
    host = (os.getenv("MAIL_HOST") or "").strip('"')
    port = int(os.getenv("MAIL_PORT", "587"))
    username = (os.getenv("MAIL_USERNAME") or "").strip('"')
    password = (os.getenv("MAIL_PASSWORD") or "").strip('"')
    encryption = (os.getenv("MAIL_ENCRYPTION") or "tls").strip('"').lower()

    if not host or not username or not password:
        return False, "SMTP not configured: set MAIL_HOST, MAIL_USERNAME, MAIL_PASSWORD"

    has_attachments = attachments and len(attachments) > 0
    msg = MIMEMultipart("mixed" if has_attachments else "alternative")
    msg["Subject"] = subject
    msg["From"] = f"{from_name} <{from_addr}>" if from_name else from_addr
    msg["To"] = to_email

    if has_attachments:
        alt = MIMEMultipart("alternative")
        alt.attach(MIMEText(plain_content, "plain"))
        if html_content:
            alt.attach(MIMEText(html_content, "html"))
        msg.attach(alt)
        for filename, content, content_type in attachments:
            main, sub = (content_type.split("/", 1) + ["octet-stream"])[:2] if "/" in content_type else ("application", "octet-stream")
            part = MIMEBase(main, sub)
            part.set_payload(content)
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", "attachment", filename=filename)
            msg.attach(part)
    else:
        msg.attach(MIMEText(plain_content, "plain"))
        if html_content:
            msg.attach(MIMEText(html_content, "html"))

    payload = msg.as_string()

    try:
        server = smtplib.SMTP(host, port, timeout=30)
        try:
            server.ehlo()
            if encryption == "tls":
                server.starttls()
                server.ehlo()
            server.login(username, password)
            server.sendmail(from_addr, [to_email], payload)
            return True, None
        finally:
            try:
                server.quit()
            except Exception:
                pass
    except Exception as e:
        return False, str(e)


def _send_via_sendgrid_api(
    to_email: str,
    subject: str,
    plain_content: str,
    html_content: Optional[str],
    from_addr: str,
    from_name: str,
    api_key: Optional[str] = None,
    attachments: Optional[List[AttachmentSpec]] = None,
) -> Tuple[bool, Optional[str]]:
    """Send using SendGrid API (avoids SMTP connection issues)."""
    key = (api_key or os.getenv("SENDGRID_API_KEY") or os.getenv("MAIL_PASSWORD", "") or "").strip('"')
    if not key or not SENDGRID_AVAILABLE:
        return False, "SendGrid not available: install sendgrid and set SENDGRID_API_KEY or MAIL_PASSWORD"

    message = Mail(
        from_email=Email(from_addr, from_name),
        to_emails=To(to_email),
        subject=subject,
        plain_text_content=Content("text/plain", plain_content),
    )
    if html_content:
        message.add_content(Content("text/html", html_content))

    if attachments:
        for filename, content, content_type in attachments:
            att = Attachment(
                file_content=FileContent(base64.b64encode(content).decode("utf-8")),
                file_name=FileName(filename),
                file_type=FileType(content_type),
                disposition="attachment",
            )
            message.add_attachment(att)

    try:
        sg = SendGridAPIClient(api_key=key)
        sg.send(message)
        return True, None
    except Exception as e:
        msg = str(e)
        if "401" in msg or "Unauthorized" in msg:
            return False, "Email provider rejected the request (invalid or expired API key). Check SENDGRID_API_KEY or MAIL_PASSWORD in .env."
        return False, msg


def send_email(
    to_email: str,
    subject: str,
    plain_content: str,
    html_content: Optional[str] = None,
    from_email: Optional[str] = None,
    from_name: Optional[str] = None,
    attachments: Optional[List[AttachmentSpec]] = None,
) -> Tuple[bool, Optional[str]]:
    """
    Send a single email. Returns (success, error_message).
    Uses SMTP (MAIL_*) when MAIL_HOST is set (Laravel .env), else SendGrid API if key set.
    attachments: optional list of (filename, raw_bytes, content_type) e.g. ("guide.pdf", pdf_bytes, "application/pdf").
    """
    to_email = (to_email or "").strip()
    if not to_email or "@" not in to_email:
        return False, "Valid recipient email is required"

    from_addr = from_email or get_from_email()
    from_name_val = from_name or get_from_name()
    atts = attachments or []

    # Prefer SendGrid API when MAIL_PASSWORD looks like an API key (SG.xxx) to avoid SMTP "Connection unexpectedly closed"
    mail_password = (os.getenv("MAIL_PASSWORD") or "").strip('"')
    if mail_password.startswith("SG.") and SENDGRID_AVAILABLE:
        return _send_via_sendgrid_api(
            to_email, subject, plain_content, html_content, from_addr, from_name_val, api_key=mail_password, attachments=atts
        )
    api_key = os.getenv("SENDGRID_API_KEY") or mail_password
    if api_key and SENDGRID_AVAILABLE:
        return _send_via_sendgrid_api(to_email, subject, plain_content, html_content, from_addr, from_name_val, api_key=api_key, attachments=atts)
    # Use SMTP (MAIL_HOST, etc.)
    host = (os.getenv("MAIL_HOST") or "").strip('"')
    if host:
        return _send_via_smtp(to_email, subject, plain_content, html_content, from_addr, from_name_val, attachments=atts)
    return False, "Email not configured: set MAIL_* (or SENDGRID_API_KEY)"


def send_pdf_email(
    to_email: str,
    pdf_type: Optional[str] = None,
    recipient_name: Optional[str] = None,
    pdf_link: Optional[str] = None,
    attachments: Optional[List[AttachmentSpec]] = None,
) -> Tuple[bool, Optional[str]]:
    """
    Send the Creator Team Building Guide email (Laravel: PdfSendMail, emails/pdf-send.blade.php).
    Used by /api/pdfsend. If pdf_link is provided, the file is fetched and attached.
    You can also pass attachments directly (e.g. from other flows).
    """
    subject = email_copies.PDF_SEND_SUBJECT
    plain, html = email_copies.pdf_send_body(recipient_name)
    all_attachments: List[AttachmentSpec] = list(attachments or [])
    if pdf_link and pdf_link.strip():
        content, err = fetch_url_as_bytes(pdf_link.strip())
        if err:
            return False, f"Could not fetch PDF from link: {err}"
        if content:
            filename = "Creator-Team-Building-Guide.pdf"
            all_attachments.append((filename, content, "application/pdf"))
    return send_email(to_email, subject, plain, html_content=html, attachments=all_attachments if all_attachments else None)


def send_verification_email(
    to_email: str,
    user_name: Optional[str],
    code: str,
    attachments: Optional[List[AttachmentSpec]] = None,
) -> Tuple[bool, Optional[str]]:
    """Laravel: Verification mailable, emails/verification.blade.php."""
    subject = email_copies.VERIFICATION_SUBJECT
    plain, html = email_copies.verification_body(user_name, code)
    return send_email(to_email, subject, plain, html_content=html, attachments=attachments)


def send_reset_email(
    to_email: str,
    user_name: Optional[str],
    code: str,
    reset_email: bool = False,
    attachments: Optional[List[AttachmentSpec]] = None,
) -> Tuple[bool, Optional[str]]:
    """Laravel: Reset mailable, emails/reset.blade.php (password or email reset)."""
    subject = email_copies.RESET_EMAIL_SUBJECT if reset_email else email_copies.RESET_PASSWORD_SUBJECT
    plain, html = email_copies.reset_body(user_name, to_email, code, reset_email=reset_email)
    return send_email(to_email, subject, plain, html_content=html, attachments=attachments)


def send_customer_invite_email(
    to_email: str,
    name: str,
    creators: List[Any],
    has_account: bool = False,
    attachments: Optional[List[AttachmentSpec]] = None,
) -> Tuple[bool, Optional[str]]:
    """Laravel: Customer mailable, emails/customer_invite*.blade.php."""
    subject = email_copies.customer_invite_subject(name)
    plain, html = email_copies.customer_invite_body(name, to_email, creators or [], has_account)
    return send_email(to_email, subject, plain, html_content=html, attachments=attachments)


def send_editor_invite_email(
    to_email: str,
    first_name: Optional[str],
    invite_url: str,
    attachments: Optional[List[AttachmentSpec]] = None,
) -> Tuple[bool, Optional[str]]:
    """Laravel: Invite mailable, emails/invite.blade.php, app.invite_subject."""
    subject = email_copies.editor_invite_subject(first_name)
    plain, html = email_copies.editor_invite_body(first_name, invite_url)
    return send_email(to_email, subject, plain, html_content=html, attachments=attachments)
