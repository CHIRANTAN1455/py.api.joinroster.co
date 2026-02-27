from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response

from app.core.dependencies import otp_rate_limit


class OtpRateLimitMiddleware(BaseHTTPMiddleware):
    """
    Middleware wrapper mirroring Laravel's `otp.rate.limit` behavior.
    Dependency-based usage is preferred for explicit control per endpoint.
    """

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        await otp_rate_limit(request)
        return await call_next(request)

