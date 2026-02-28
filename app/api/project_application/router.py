from fastapi import APIRouter, Depends

from app.core.dependencies import require_auth, unlimited_rate


router = APIRouter(prefix="/project-application", tags=["project-application"])


@router.get("", dependencies=[Depends(require_auth)])
def list_project_applications():
    """
    GET /project-application
    Middleware: auth:sanctum
    """
    return {"status": "success"}


@router.get("/{id}", dependencies=[Depends(require_auth)])
def get_project_application(id: int):
    """
    GET /project-application/{id}
    Middleware: auth:sanctum
    """
    return {"status": "success", "id": id}


@router.post("/add", dependencies=[Depends(require_auth)])
def add_project_application():
    """
    POST /project-application/add
    Middleware: auth:sanctum
    """
    return {"status": "success"}


@router.patch("/{id}", dependencies=[Depends(require_auth)])
def update_project_application(id: int):
    """
    PATCH /project-application/{id}
    Middleware: auth:sanctum
    """
    return {"status": "success", "id": id}


@router.post("/{id}/note", dependencies=[Depends(require_auth)])
def add_project_application_note(id: int):
    """
    POST /project-application/{id}/note
    Middleware: auth:sanctum
    """
    return {"status": "success", "id": id}


@router.delete("/note/{id}", dependencies=[Depends(require_auth)])
def delete_project_application_note(id: int):
    """
    DELETE /project-application/note/{id}
    Middleware: auth:sanctum
    """
    return {"status": "success", "id": id}


@router.post(
    "/rejection",
    dependencies=[Depends(require_auth), Depends(unlimited_rate)],
)
def project_application_rejection():
    """
    POST /project-application/rejection
    Middleware: auth:sanctum, api.unlimited
    """
    return {"status": "success"}

