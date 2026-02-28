from fastapi import APIRouter, Depends

from app.core.dependencies import require_auth


router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/editors", dependencies=[Depends(require_auth)])
def list_editors():
    """
    GET /admin/editors
    Middleware: auth:sanctum
    """
    return {"status": "success"}


@router.get("/editors/{id}", dependencies=[Depends(require_auth)])
def get_editor(id: int):
    """
    GET /admin/editors/{id}
    Middleware: auth:sanctum
    """
    return {"status": "success", "id": id}


@router.get("/creators/{id}", dependencies=[Depends(require_auth)])
def get_creator(id: int):
    """
    GET /admin/creators/{id}
    Middleware: auth:sanctum
    """
    return {"status": "success", "id": id}


@router.get("/creators", dependencies=[Depends(require_auth)])
def list_creators():
    """
    GET /admin/creators
    Middleware: auth:sanctum
    """
    return {"status": "success"}


@router.get("/projects", dependencies=[Depends(require_auth)])
def list_projects():
    """
    GET /admin/projects
    Middleware: auth:sanctum
    """
    return {"status": "success"}


@router.get("/projects/{id}", dependencies=[Depends(require_auth)])
def get_project_admin(id: int):
    """
    GET /admin/projects/{id}
    Middleware: auth:sanctum
    """
    return {"status": "success", "id": id}


@router.delete("/editors/{email}", dependencies=[Depends(require_auth)])
def delete_editor(email: str):
    """
    DELETE /admin/editors/{email}
    Middleware: auth:sanctum
    """
    return {"status": "success", "email": email}


@router.post("/users/email", dependencies=[Depends(require_auth)])
def admin_users_email():
    """
    POST /admin/users/email
    Middleware: auth:sanctum
    """
    return {"status": "success"}

