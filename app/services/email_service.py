"""
Email sending: SMTP (Laravel MAIL_*) or SendGrid API.
Uses .env: MAIL_HOST, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD, MAIL_FROM_ADDRESS, MAIL_FROM_NAME.
With MAIL_HOST=smtp.sendgrid.net and MAIL_PASSWORD=SendGrid API key, no extra config needed.
"""
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional, Tuple

try:
    from sendgrid import SendGridAPIClient
    from sendgrid.helpers.mail import Mail, Email, To, Content
    SENDGRID_AVAILABLE = True
except ImportError:
    SENDGRID_AVAILABLE = False


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
) -> Tuple[bool, Optional[str]]:
    """Send using SMTP (MAIL_HOST, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD)."""
    host = (os.getenv("MAIL_HOST") or "").strip('"')
    port = int(os.getenv("MAIL_PORT", "587"))
    username = (os.getenv("MAIL_USERNAME") or "").strip('"')
    password = (os.getenv("MAIL_PASSWORD") or "").strip('"')
    encryption = (os.getenv("MAIL_ENCRYPTION") or "tls").strip('"').lower()

    if not host or not username or not password:
        return False, "SMTP not configured: set MAIL_HOST, MAIL_USERNAME, MAIL_PASSWORD"

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"{from_name} <{from_addr}>" if from_name else from_addr
    msg["To"] = to_email
    msg.attach(MIMEText(plain_content, "plain"))
    if html_content:
        msg.attach(MIMEText(html_content, "html"))

    try:
        if encryption == "tls":
            with smtplib.SMTP(host, port) as server:
                server.starttls()
                server.login(username, password)
                server.sendmail(from_addr, to_email, msg.as_string())
        else:
            with smtplib.SMTP(host, port) as server:
                server.login(username, password)
                server.sendmail(from_addr, to_email, msg.as_string())
        return True, None
    except Exception as e:
        return False, str(e)


def _send_via_sendgrid_api(
    to_email: str,
    subject: str,
    plain_content: str,
    html_content: Optional[str],
    from_addr: str,
    from_name: str,
) -> Tuple[bool, Optional[str]]:
    """Send using SendGrid API (SENDGRID_API_KEY)."""
    api_key = os.getenv("SENDGRID_API_KEY") or os.getenv("MAIL_PASSWORD", "").strip('"')
    if not api_key or not SENDGRID_AVAILABLE:
        return False, "SendGrid not available: install sendgrid and set SENDGRID_API_KEY or MAIL_PASSWORD"

    message = Mail(
        from_email=Email(from_addr, from_name),
        to_emails=To(to_email),
        subject=subject,
        plain_text_content=Content("text/plain", plain_content),
    )
    if html_content:
        message.add_content(Content("text/html", html_content))

    try:
        sg = SendGridAPIClient(api_key=api_key)
        sg.send(message)
        return True, None
    except Exception as e:
        return False, str(e)


def send_email(
    to_email: str,
    subject: str,
    plain_content: str,
    html_content: Optional[str] = None,
    from_email: Optional[str] = None,
    from_name: Optional[str] = None,
) -> Tuple[bool, Optional[str]]:
    """
    Send a single email. Returns (success, error_message).
    Uses SMTP (MAIL_*) when MAIL_HOST is set (Laravel .env), else SendGrid API if key set.
    """
    to_email = (to_email or "").strip()
    if not to_email or "@" not in to_email:
        return False, "Valid recipient email is required"

    from_addr = from_email or get_from_email()
    from_name_val = from_name or get_from_name()

    # Prefer SMTP when Laravel MAIL_* is set (e.g. MAIL_HOST=smtp.sendgrid.net, MAIL_PASSWORD=SendGrid key)
    host = (os.getenv("MAIL_HOST") or "").strip('"')
    if host:
        return _send_via_smtp(to_email, subject, plain_content, html_content, from_addr, from_name_val)
    # Fallback to SendGrid API
    return _send_via_sendgrid_api(to_email, subject, plain_content, html_content, from_addr, from_name_val)


def send_pdf_email(
    to_email: str,
    pdf_type: Optional[str] = None,
    recipient_name: Optional[str] = None,
) -> Tuple[bool, Optional[str]]:
    """
    Send the "PDF" email (e.g. invoice, document link).
    Used by /api/pdfsend.
    """
    subject = "Your document"
    if pdf_type:
        subject = f"Your {pdf_type}"
    name = recipient_name or "there"
    plain = f"Hello {name},\n\nPlease find your requested document attached or via the link below.\n\nBest regards,\n{get_from_name()}"
    html = f"<p>Hello {name},</p><p>Please find your requested document attached or via the link below.</p><p>Best regards,<br>{get_from_name()}</p>"
    return send_email(to_email, subject, plain, html_content=html)
