from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from app.api.auth.router import router as auth_router
from app.api.project.router import router as project_router
from app.core.config import get_settings
from app.core.cors import configure_cors


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

    # Include domain routers (tags defined in each router module).
    app.include_router(auth_router)
    app.include_router(project_router)

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

