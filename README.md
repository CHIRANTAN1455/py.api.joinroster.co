# py.api.joinroster.co

FastAPI reimplementation of the existing Laravel backend located at `Desktop/api.joinroster.co`.

## Overview

- **1:1 routes**: Every Laravel API route is mirrored with the same HTTP method, path, parameters, and semantics.
- **Response parity**: JSON keys, casing, nesting, pagination, and validation error formats are designed to match Laravel exactly, based on `fastapi_migration_spec.json`.
- **Auth model**: `auth:sanctum` is represented via JWT bearer auth, with per-route dependencies enforcing authentication.
- **Rate limiting**: Laravel middleware groups (`api.strict`, `api.lenient`, `api.unlimited`, `api.otp`) are mapped to FastAPI dependencies and optional middleware.
- **CORS**: Fully open CORS configuration (all origins, methods, headers, credentials).

## Local development

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Celery worker:

```bash
celery -A jobs.celery_app.celery_app worker --loglevel=info
```

Further domain routers, controllers, schemas, and services are implemented under `app/api` and `app/services`, following the structure described in `fastapi_migration_spec.json`.

