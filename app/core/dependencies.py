from time import time
from typing import Dict

import jwt
from fastapi import Depends, HTTPException, Request, status

from app.core.config import get_settings
from app.core.security import get_current_user_token

# Very simple in-memory rate limiting buckets keyed by client identifier.
# For production you should back this with Redis to match Laravel's
# ApiRateLimit and OtpRateLimit middleware behavior.
_rate_buckets: Dict[str, Dict[str, float]] = {}


def _rate_limit(request: Request, key_prefix: str, max_attempts: int, decay_seconds: int) -> None:
    client_id = request.client.host or "unknown"
    key = f"{key_prefix}:{client_id}"
    now = time()
    bucket = _rate_buckets.get(key)

    if bucket is None or now - bucket["start"] > decay_seconds:
        _rate_buckets[key] = {"start": now, "count": 1}
        return

    if bucket["count"] >= max_attempts:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail={"status": "error", "message": "Too Many Attempts."},
        )

    bucket["count"] += 1


async def ensure_stateful_request(request: Request) -> None:
    """
    Lightweight analogue for Laravel's EnsureFrontendRequestsAreStateful.
    This checks for the presence of cookies or Authorization headers to
    ensure the request is associated with a client session.
    """
    if not request.cookies and "authorization" not in request.headers:
        # Laravel usually allows non-stateful too, but when this is applied
        # we enforce that at least some client state is present.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"status": "error", "message": "Unauthenticated."},
        )


async def strict_rate_limit(request: Request, _: None = Depends(ensure_stateful_request)) -> None:
    """
    Match Laravel `api.strict` group: ApiRateLimit 10 requests per minute.
    """
    _rate_limit(request, key_prefix="strict", max_attempts=10, decay_seconds=60)


async def lenient_rate_limit(request: Request, _: None = Depends(ensure_stateful_request)) -> None:
    """
    Match Laravel `api.lenient` group: ApiRateLimit 120 requests per minute.
    """
    _rate_limit(request, key_prefix="lenient", max_attempts=120, decay_seconds=60)


async def unlimited_rate(request: Request, _: None = Depends(ensure_stateful_request)) -> None:  # noqa: ARG001
    """
    Match Laravel `api.unlimited` group: Ensure stateful but no throttling.
    """
    return None


async def otp_rate_limit(request: Request, _: None = Depends(ensure_stateful_request)) -> None:
    """
    Rough analogue of Laravel's OtpRateLimit. We approximate the most
    restrictive bucket and can refine per-path later if needed.
    """
    _rate_limit(request, key_prefix="otp", max_attempts=5, decay_seconds=15 * 60)


async def require_auth(token: str = Depends(get_current_user_token)) -> str:
    """
    Wrapper dependency for `auth:sanctum` routes. Returns the validated
    JWT bearer token; controller/service layers can then resolve the user.
    """
    return token


async def get_current_user_id(token: str = Depends(get_current_user_token)) -> int:
    """
    Decode the validated JWT token and return the numeric user ID from `sub`.
    This is used by controllers that need the authenticated user ID, while
    still preserving `require_auth` as a pure-guard dependency.
    """
    settings = get_settings()
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"status": "error", "message": "Invalid token."},
        )

    sub = payload.get("sub")
    try:
        return int(sub)
    except (TypeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"status": "error", "message": "Invalid token subject."},
        )

