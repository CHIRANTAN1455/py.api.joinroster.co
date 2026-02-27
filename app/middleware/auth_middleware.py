from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response


class AuthSanctumMiddleware(BaseHTTPMiddleware):
    """
    Middleware wrapper corresponding loosely to Laravel's `auth:sanctum`.
    In practice we rely on FastAPI dependencies for per-route auth, so this
    middleware currently acts as a no-op pass-through.
    """

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        response = await call_next(request)
        return response

