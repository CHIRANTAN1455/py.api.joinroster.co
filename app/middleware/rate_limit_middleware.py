from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response

from app.core.dependencies import strict_rate_limit, lenient_rate_limit, unlimited_rate


class ApiStrictRateLimitMiddleware(BaseHTTPMiddleware):
    """
    Optional global middleware analogue for the `api.strict` group. We prefer
    dependency-based rate limiting, but this can be enabled if needed.
    """

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        await strict_rate_limit(request)
        return await call_next(request)


class ApiLenientRateLimitMiddleware(BaseHTTPMiddleware):
    """
    Analogue for the `api.lenient` middleware group.
    """

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        await lenient_rate_limit(request)
        return await call_next(request)


class ApiUnlimitedRateLimitMiddleware(BaseHTTPMiddleware):
    """
    Analogue for the `api.unlimited` middleware group.
    """

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        await unlimited_rate(request)
        return await call_next(request)

