"""
Laravel email copies: subject lines and body content (HTML/plain) matching
resources/views/emails/*.blade.php and app/Mail/*.php exactly.
"""
from __future__ import annotations

from typing import List, Optional, Tuple

APP_TITLE = "Roster"
SUPPORT_LINK = "https://www.joinroster.co/contact-us"
ROSTER_HOME = "https://www.joinroster.co"
GET_STARTED_URL = "https://app.joinroster.co/get-started"
DISCORD_INVITE = "https://discord.com/invite/ErmPaSTk"
REFERRAL_2026 = "https://www.joinroster.co/?referral=2026hiringguide"


# ——— PDF Send (emails/pdf-send.blade.php, PdfSendMail) ———
PDF_SEND_SUBJECT = "Your Creator Team Building Guide is here!"


def pdf_send_body(first_name: Optional[str]) -> Tuple[str, str]:
    name = first_name or "there"
    plain = f"""Hey {name},

Thanks for grabbing the Creator Team Building Guide 2026 - you're not alone if you're feeling stretched trying to do everything yourself.

This guide was built using insights from thousands of real creator hires on Roster, combined with Beacons' experience supporting millions of creators. It's designed to help you make clearer decisions about when to get support, who to hire first, and how to scale without burning out.

Inside, you'll learn:
- How to tell when it's time to get help (before burnout hits)
- When AI can support your workflow and when human teammates matter more
- Who creators typically hire first at different stages of growth
- What hiring actually costs (with real-world benchmarks)
- Simple checklists to help you interview, onboard, and set new hires up for success

You'll find the guide attached to this email.

As a bonus, you'll also get 30 days of free access to Roster - get started here: {REFERRAL_2026}

Wishing you more creative space and fewer late nights,

Sherry
Founder & CEO, Roster

---
This was sent with our automated system. If you need help, please contact support here: {SUPPORT_LINK} instead of replying to this email."""

    html = f"""<p>Hey {name},</p>
<p>Thanks for grabbing the <strong>Creator Team Building Guide 2026</strong> - you're not alone if you're feeling stretched trying to do everything yourself.</p>
<p>This guide was built using insights from thousands of real creator hires on Roster, combined with Beacons' experience supporting millions of creators. It's designed to help you make clearer decisions about <strong>when to get support, who to hire first, and how to scale without burning out</strong>.</p>
<p>Inside, you'll learn:</p>
<ul>
<li>How to tell when it's time to get help (before burnout hits)</li>
<li>When AI can support your workflow and when human teammates matter more</li>
<li>Who creators typically hire first at different stages of growth</li>
<li>What hiring actually costs (with real-world benchmarks)</li>
<li>Simple checklists to help you interview, onboard, and set new hires up for success</li>
</ul>
<p>You'll find the guide attached to this email.</p>
<p>As a bonus, you'll also get 30 days of free access to Roster - get started <a href="{REFERRAL_2026}" target="_blank">here</a>.</p>
<p>Wishing you more creative space and fewer late nights,</p>
<p><strong>Sherry</strong><br>Founder & CEO, Roster</p>
<p style="padding-top: 48px; font-size: 14px; text-align: center"><small style="color: #98A2B3">This was sent with our automated system. If you need help, please <a href="{SUPPORT_LINK}">contact support here</a> instead of replying to this email.</small></p>"""
    return plain, html


# ——— Verification (emails/verification.blade.php, Verification mail) ———
VERIFICATION_SUBJECT = "Verify Account"


def verification_body(user_name: Optional[str], code: str) -> Tuple[str, str]:
    name = user_name or "there"
    plain = f"""Your {APP_TITLE} account verification code

Hi {name},

To complete your registration, enter this verification code:

{code}

Thanks,
{APP_TITLE}

---
This was sent with our automated system. If you need help, please contact support here: {SUPPORT_LINK} instead of replying to this email."""

    html = f"""<h1>Your {APP_TITLE} account verification code</h1>
<p>Hi {name},</p>
<p>To complete your registration, enter this verification code:</p>
<p><strong style="font-size: 24px">{code}</strong></p>
<p>Thanks,<br>{APP_TITLE}</p>
<p style="padding-top: 48px; font-size: 14px; text-align: center"><small style="color: #98A2B3">This was sent with our automated system. If you need help, please <a href="{SUPPORT_LINK}">contact support here</a> instead of replying to this email.</small></p>"""
    return plain, html


# ——— Reset password / Reset email (emails/reset.blade.php, Reset mail) ———
RESET_PASSWORD_SUBJECT = "Reset Password"
RESET_EMAIL_SUBJECT = "Reset Email"


def reset_body(user_name: Optional[str], user_email: str, code: str, reset_email: bool = False) -> Tuple[str, str]:
    name = user_name or "there"
    action = "email" if reset_email else "password"
    plain = f"""Your {APP_TITLE} account verification code

Hi {name},

To reset your {action}, enter this verification code:

{code}

Have questions or need help? Just reply to this email - we're here for you.

Thanks,
{APP_TITLE}

This email was sent to {user_email} because you interacted with {APP_TITLE} services."""

    html = f"""<h1>Your {APP_TITLE} account verification code</h1>
<p>Hi {name},</p>
<p>To reset your {action}, enter this verification code:</p>
<p><strong style="font-size: 24px">{code}</strong></p>
<p>Have questions or need help? Just reply to this email - we're here for you.</p>
<p>Thanks,<br>{APP_TITLE}</p>
<p><small>This email was sent to {user_email} because you interacted with {APP_TITLE} services.</small></p>"""
    return plain, html


# ——— Customer invite (emails/customer_invite, customer_invite_with_account) ———
def customer_invite_subject(recipient_name: str) -> str:
    return f"your hiring recommendations - {recipient_name}"


def customer_invite_body(name: str, email: str, creators: List, has_account: bool) -> Tuple[str, str]:
    """creators: list of dicts with name, username, title, photo (optional)."""
    if not creators:
        creator_block_plain = "We'll have recommendations for you soon."
        creator_block_html = "<p>We'll have recommendations for you soon.</p>"
    else:
        lines = []
        for c in creators:
            n = c.get("name") or c.get("username", "")
            t = c.get("title") or ""
            if n and t:
                lines.append(f"- {n} - {t}")
            else:
                lines.append(f"- {n}" if n else "- Creator")
        creator_block_plain = "\n".join(lines)
        creator_block_html = "<ul>" + "".join(
            "<li>{} - {}</li>".format(c.get("name") or c.get("username", ""), c.get("title", "")) for c in creators
        ) + "</ul>"

    if has_account:
        plain = f"""Hi {name},

Based on your content style preferences, here are some top recommendations for you:

{creator_block_plain}

What's next:
You'll be able to bookmark profiles and get even better personalized recommendations if you complete your profile here (takes 2 minutes).

Complete profile: {ROSTER_HOME}/discover

Did you know? Our platform is home to Video Editors, Thumbnail Designers, and Scriptwriters who work for the world's biggest creators like MrBeast, Dude Perfect, and more.

Cheers,
The Roster Team

This email was sent to {email} because you interacted with Roster services."""

        html = f"""<p style="margin-bottom: 16px">Hi {name},</p>
<p>Based on your content style preferences, here are some top recommendations for you:</p>
<div style="margin-bottom: 32px">{creator_block_html}</div>
<p><b>What's next:</b></p>
<p>You'll be able to bookmark profiles and get even better personalized recommendations if you complete your profile here (takes 2 minutes).</p>
<p><a href="{ROSTER_HOME}/discover">Complete profile</a></p>
<p>Did you know? Our platform is home to Video Editors, Thumbnail Designers, and Scriptwriters who work for the world's biggest creators like MrBeast, Dude Perfect, and more.</p>
<div style="margin-top: 32px">Cheers,</div>
<div>The Roster Team</div>
<p><small>This email was sent to {email} because you interacted with Roster services.</small></p>"""
    else:
        plain = f"""Hi {name},

Based on your content style preferences, here are some top recommendations for you:

{creator_block_plain}

Want to explore more profiles? Create your account - it only takes 2 minutes and it's free.

Complete profile: {GET_STARTED_URL}

Once you make an account, you can also bookmark talent recommendations and post jobs.

Did you know? Our platform is home to Video Editors, Thumbnail Designers, and Scriptwriters who work for the world's biggest creators like MrBeast, Dude Perfect, and more.

Cheers,
The Roster Team

This email was sent to {email} because you interacted with Roster services."""

        html = f"""<p style="margin-bottom: 16px">Hi {name},</p>
<p>Based on your content style preferences, here are some top recommendations for you:</p>
<div style="margin-bottom: 32px">{creator_block_html}</div>
<p>Want to explore more profiles? Create your account - it only takes 2 minutes and it's free.</p>
<p><a href="{GET_STARTED_URL}">Complete profile</a></p>
<p>Once you make an account, you can also bookmark talent recommendations and post jobs.</p>
<p>Did you know? Our platform is home to Video Editors, Thumbnail Designers, and Scriptwriters who work for the world's biggest creators like MrBeast, Dude Perfect, and more.</p>
<div style="margin-top: 32px">Cheers,</div>
<div>The Roster Team</div>
<p><small>This email was sent to {email} because you interacted with Roster services.</small></p>"""
    return plain, html


# ——— Editor invite (emails/invite.blade.php, Invite mail, app.invite_subject) ———
def editor_invite_subject(first_name: Optional[str]) -> str:
    name = first_name or "you"
    return f"Your wait is over! 🚀 Invitation for {name} to Roster"


def editor_invite_body(first_name: Optional[str], url: str) -> Tuple[str, str]:
    name = first_name or "there"
    plain = f"""Hi {name},

We are thrilled to announce that Roster is ready for you to use and it's time to get started!

As a valued member of our community, we've selected a small handful of you to receive first exclusive access to our platform and you're one of them.

Please use this unique link to get started: {url}

With your new account, you'll be able to discover and connect with other creatives & creators, and claim your own unique username.

We can't wait for you to start using Roster! If you have any questions or need assistance, simply reply to this email and our support team will be here to help.

Lastly, don't forget to join our invite-only Discord community: {DISCORD_INVITE}

Cheers,
The Roster Team

If you're having trouble clicking the "unique link", copy and paste the URL below into your web browser: {url}"""

    html = f"""<p>Hi {name},</p>
<p>We are thrilled to announce that Roster is ready for you to use and it's time to get started!</p>
<p>As a valued member of our community, we've selected a small handful of you to receive first exclusive access to our platform and you're one of them.</p>
<p>Please use this <a href="{url}">unique link</a> to get started. With your new account, you'll be able to discover and connect with other creatives & creators, and claim your own unique username.</p>
<p>We can't wait for you to start using Roster! If you have any questions or need assistance, simply reply to this email and our support team will be here to help.</p>
<p>Lastly, don't forget to join our invite-only <a href="{DISCORD_INVITE}">Discord community</a> to chat with others!</p>
<p>Cheers,<br>The Roster Team</p>
<p><small>If you're having trouble clicking the "unique link", copy and paste the URL below into your web browser: {url}</small></p>"""
    return plain, html
