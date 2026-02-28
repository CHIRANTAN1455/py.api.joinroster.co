from fastapi import APIRouter, Depends

from app.core.dependencies import require_auth


router = APIRouter(prefix="/userproject", tags=["userproject"])


@router.get("/public/info")
def userproject_public_info():
    """
    GET /userproject/public/info
    Middleware: none
    """
    return {"status": "success"}


@router.get("/public")
def userproject_public():
    """
    GET /userproject/public
    Middleware: none
    """
    return {"status": "success"}


@router.get("", dependencies=[Depends(require_auth)])
def list_userprojects():
    """
    GET /userproject
    Middleware: auth:sanctum
    """
    return {"status": "success"}


@router.get("/info", dependencies=[Depends(require_auth)])
def userproject_info():
    """
    GET /userproject/info
    Middleware: auth:sanctum
    """
    return {"status": "success"}


@router.post("", dependencies=[Depends(require_auth)])
def create_userproject():
    """
    POST /userproject
    Middleware: auth:sanctum
    """
    return {"status": "success"}


@router.post("/{id}/update", dependencies=[Depends(require_auth)])
def update_userproject(id: int):
    """
    POST /userproject/{id}/update
    Middleware: auth:sanctum
    """
    return {"status": "success", "id": id}


@router.delete("/{id}", dependencies=[Depends(require_auth)])
def delete_userproject(id: int):
    """
    DELETE /userproject/{id}
    Middleware: auth:sanctum
    """
    return {"status": "success", "id": id}

