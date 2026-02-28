from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse

from app.api.auth.router import router as auth_router
from app.api.project.router import router as project_router
from app.api.profile.router import router as profile_router
from app.api.chat.router import router as chat_router
from app.api.matching.router import router as matching_router
from app.api.project_application.router import router as project_application_router
from app.api.user.router import router as user_router
from app.api.admin.router import router as admin_router
from app.api.public.router import router as public_router
from app.api.lookups.router import router as lookups_router
from app.api.customer.router import router as customer_router
from app.api.userproject.router import router as userproject_router
from app.api.usercreator.router import router as usercreator_router
from app.api.social.router import router as social_router
from app.api.payment.router import router as payment_router
from app.api.userverification.router import router as userverification_router
from app.api.referral.router import router as referral_router
from app.api.editor.router import router as editor_router
from app.api.favourite.router import router as favourite_router
from app.api.file.router import router as file_router
from app.api.questionnaire.router import router as questionnaire_router
from app.api.project_screening.router import router as project_screening_router
from app.api.job_posting_edit.router import router as job_posting_edit_router
from app.api.user_todo.router import router as user_todo_router
from app.api.shortlist.router import router as shortlist_router
from app.api.profile_visit.router import router as profile_visit_router
from app.api.data.router import router as data_router
from app.api.health.router import router as health_router
from app.core.config import get_settings
from app.core.cors import configure_cors
from app.core.laravel_response import validation_error_body


def _laravel_validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Return Laravel-exact validation error: status, message, fields (400)."""
    errors: dict = {}
    all_msgs: list = []
    for e in exc.errors():
        loc = e.get("loc", ())
        # loc is e.g. ("body", "email") or ("query", "page"); use last part as field name
        field = loc[-1] if loc else "field"
        if isinstance(field, int):
            field = str(field)
        msg = e.get("msg", "Validation error")
        errors.setdefault(field, []).append(msg)
        all_msgs.append(msg)
    body = validation_error_body(
        message=" | ".join(all_msgs),
        errors=errors,
    )
    return JSONResponse(status_code=400, content=body)


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title=settings.APP_NAME,
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    configure_cors(app)

    app.add_exception_handler(RequestValidationError, _laravel_validation_exception_handler)

    # Include domain routers under a common `/api` base path so every
    # endpoint is exposed as `<domain>/api/<endpoint>` on the host.
    app.include_router(auth_router, prefix="/api")
    app.include_router(project_router, prefix="/api")
    app.include_router(profile_router, prefix="/api")
    app.include_router(chat_router, prefix="/api")
    app.include_router(matching_router, prefix="/api")
    app.include_router(project_application_router, prefix="/api")
    app.include_router(user_router, prefix="/api")
    app.include_router(admin_router, prefix="/api")
    app.include_router(public_router, prefix="/api")
    app.include_router(lookups_router, prefix="/api")
    app.include_router(customer_router, prefix="/api")
    app.include_router(userproject_router, prefix="/api")
    app.include_router(usercreator_router, prefix="/api")
    app.include_router(social_router, prefix="/api")
    app.include_router(payment_router, prefix="/api")
    app.include_router(userverification_router, prefix="/api")
    app.include_router(referral_router, prefix="/api")
    app.include_router(editor_router, prefix="/api")
    app.include_router(favourite_router, prefix="/api")
    app.include_router(file_router, prefix="/api")
    app.include_router(questionnaire_router, prefix="/api")
    app.include_router(project_screening_router, prefix="/api")
    app.include_router(job_posting_edit_router, prefix="/api")
    app.include_router(user_todo_router, prefix="/api")
    app.include_router(shortlist_router, prefix="/api")
    app.include_router(profile_visit_router, prefix="/api")
    app.include_router(data_router, prefix="/api")
    app.include_router(health_router, prefix="/api")

    return app


app = create_app()


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        routes=app.routes,
    )

    # JWT auth scheme for Swagger / OpenAPI docs
    openapi_schema.setdefault("components", {}).setdefault("securitySchemes", {})[
        "BearerAuth"
    ] = {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT",
    }

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi  # type: ignore[assignment]

