"""
Laravel-exact API response formatting.

Laravel's api() helper is response()->json($data, $code) — no wrapper.
All keys, casing, and structure must match Laravel 1:1.
"""

from typing import Any, Dict, Optional


def user_to_laravel_user_resource(user: Any) -> Dict[str, Any]:
    """
    Build a dict matching Laravel's UserResource::toArray() keys exactly.
    Uses None for missing fields so JSON outputs null. Key order matches Laravel.
    """
    return {
        "uuid": getattr(user, "uuid", None),
        "photo": getattr(user, "photo", None),
        "name": getattr(user, "name", None),
        "first_name": getattr(user, "first_name", None),
        "last_name": getattr(user, "last_name", None),
        "dob": getattr(user, "dob", None),
        "gender": getattr(user, "gender", None),
        "email": getattr(user, "email", None),
        "email_verified_at": getattr(user, "email_verified_at", None),
        "phone": getattr(user, "phone", None),
        "phone_verified_at": getattr(user, "phone_verified_at", None),
        "address": getattr(user, "address", None),
        "city": getattr(user, "city", None),
        "country": getattr(user, "country", None),
        "company": getattr(user, "company", None),
        "job_title": getattr(user, "job_title", None),
        "username": getattr(user, "username", None),
        "fun_fact": getattr(user, "fun_fact", None),
        "created_at": getattr(user, "created_at", None),
        "updated_at": getattr(user, "updated_at", None),
        "activated_at": getattr(user, "activated_at", None),
        "is_activated": getattr(user, "activated_at", None) is not None,
        "verified_at": getattr(user, "verified_at", None),
        "is_verified": getattr(user, "verified_at", None) is not None,
        "open_for_work": getattr(user, "open_for_work", None),
        "active": getattr(user, "active", True),
        "completion": getattr(user, "completion", None),
        "account_type": getattr(user, "account_type", None),
        "reference": getattr(user, "reference", None),
        "utc_offset": getattr(user, "utc_offset", None),
        "timezone": getattr(user, "timezone", None),
        "referral_code": getattr(user, "referral_code", None),
        "pricing": None,
        "skills": [],
        "job_types": [],
        "content_verticals": [],
        "platforms": [],
        "softwares": [],
        "equipments": [],
        "creative_styles": [],
        "social_profiles": None,
        "customer": None,
        "creators": [],
        "has_creators": False,
        "has_min_1_project": False,
        "has_min_3_projects": False,
        "has_creators_with_projects": None,
        "has_creative_styles": False,
        "has_creator_with_details": False,
        "resume": getattr(user, "resume", None),
        "resume_updated_at": getattr(user, "resume_updated_at", None),
        "worked_with_creators": getattr(user, "worked_with_creators", None),
        "new_onboarding": getattr(user, "new_onboarding", None),
        "count_non_youtube_projects": 0,
        "via_affiliate": getattr(user, "via_affiliate", None),
        "email_unsubscriptions": getattr(user, "email_unsubscriptions", None),
        "import_via_linkedin": getattr(user, "import_via_linkedin", None),
        "import_via_resume": getattr(user, "import_via_resume", None),
        "languages": [],
        "policy_accepted": getattr(user, "policy_accepted", None),
        "policy_accepted_at": getattr(user, "policy_accepted_at", None),
        "referral_count": 0,
    }


def api_success(
    payload: Dict[str, Any],
    status_code: int = 200,
) -> Dict[str, Any]:
    """
    Return a dict that will be JSON-serialized exactly as Laravel would.
    Do not add or remove keys; do not change casing.
    payload must already contain 'status': 'success' and any 'message', 'user', etc.
    """
    return payload


def api_error(
    message: str,
    status_code: int = 400,
    fields: Optional[Dict[str, list]] = None,
) -> Dict[str, Any]:
    """
    Laravel validation/error shape from Validation.php and typical API errors:
    - status: "error"
    - message: string
    - fields: optional dict of field -> list of error strings (Laravel uses "fields" in this codebase)
    """
    out: Dict[str, Any] = {"status": "error", "message": message}
    if fields is not None:
        out["fields"] = fields
    return out


def validation_error_body(message: str, errors: Dict[str, list]) -> Dict[str, Any]:
    """
    Exact shape returned by Laravel when Validation::api fails:
    status, message, fields (field name -> list of messages).
    """
    return {"status": "error", "message": message, "fields": errors}


def success_with_message(message: str, **extra: Any) -> Dict[str, Any]:
    """Laravel pattern: status, message, then any extra keys (e.g. user, project, matching)."""
    out: Dict[str, Any] = {"status": "success", "message": message}
    out.update(extra)
    return out


def skill_to_laravel_skill_resource(skill: Any) -> Dict[str, Any]:
    """Skill resource: uuid, icon, name, description (no integer id)."""
    return {
        "uuid": getattr(skill, "uuid", None),
        "icon": getattr(skill, "icon", None),
        "name": getattr(skill, "name", None),
        "description": getattr(skill, "description", None),
    }


def lookup_to_laravel_resource(record: Any) -> Dict[str, Any]:
    """Generic lookup (content_vertical, platform, software, equipment, creative_style, content_form, job_type): uuid, icon, name, description."""
    return {
        "uuid": getattr(record, "uuid", None),
        "icon": getattr(record, "icon", None),
        "name": getattr(record, "name", None),
        "description": getattr(record, "description", None),
    }


def project_type_to_laravel_resource(record: Any) -> Dict[str, Any]:
    """ProjectTypeResource: uuid, icon, name, description, count."""
    return {
        "uuid": getattr(record, "uuid", None),
        "icon": getattr(record, "icon", None),
        "name": getattr(record, "name", None),
        "description": getattr(record, "description", None),
        "count": getattr(record, "count", 0),
    }


def reason_to_laravel_resource(record: Any) -> Dict[str, Any]:
    """ReasonResource: uuid, name, description."""
    return {
        "uuid": getattr(record, "uuid", None),
        "name": getattr(record, "name", None),
        "description": getattr(record, "description", None),
    }


def referral_to_laravel_resource(record: Any) -> Dict[str, Any]:
    """ReferralResource: uuid, name, priority, require_input, description."""
    return {
        "uuid": getattr(record, "uuid", None),
        "name": getattr(record, "name", None),
        "priority": getattr(record, "priority", None),
        "require_input": getattr(record, "require_input", None),
        "description": getattr(record, "description", None),
    }


def location_to_laravel_resource(record: Any) -> Dict[str, Any]:
    """LocationResource: uuid, location (city_ascii, country), city, city_ascii, country."""
    city_ascii = getattr(record, "city_ascii", None) or ""
    country = getattr(record, "country", None) or ""
    return {
        "uuid": getattr(record, "uuid", None),
        "location": f"{city_ascii}, {country}".strip(", "),
        "city": getattr(record, "city", None),
        "city_ascii": city_ascii,
        "country": country,
    }

