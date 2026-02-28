from fastapi import APIRouter, Depends

from app.core.dependencies import require_auth


router = APIRouter(prefix="/matching", tags=["matching"])


@router.get("", dependencies=[Depends(require_auth)])
def search_matching():
    """
    GET /matching
    Middleware: auth:sanctum
    """
    return {"status": "success"}


@router.get("/project/{id}", dependencies=[Depends(require_auth)])
def get_matching_project(id: int):
    """
    GET /matching/project/{id}
    Middleware: auth:sanctum
    """
    return {"status": "success", "id": id}


@router.patch("/editor", dependencies=[Depends(require_auth)])
def update_matching_editor():
    """
    PATCH /matching/editor
    Middleware: auth:sanctum
    """
    return {"status": "success"}


@router.post("/public-matching")
def public_matching():
    """
    POST /public-matching
    Middleware: none
    """
    return {"status": "success"}


@router.get("/{id}")
def get_matching(id: int):
    """
    GET /matching/{id}
    Middleware: none
    """
    return {"status": "success", "id": id}


@router.get("/token/{token}")
def get_matching_by_token(token: str):
    """
    GET /matching/token/{token}
    Middleware: none
    """
    return {"status": "success", "token": token}


@router.post("", dependencies=[Depends(require_auth)])
def create_matching():
    """
    POST /matching
    Middleware: auth:sanctum
    """
    return {"status": "success"}


@router.post("/creators", dependencies=[Depends(require_auth)])
def matching_creators():
    """
    POST /matching/creators
    Middleware: auth:sanctum
    """
    return {"status": "success"}


@router.patch("/{id}", dependencies=[Depends(require_auth)])
def update_matching(id: int):
    """
    PATCH /matching/{id}
    Middleware: auth:sanctum
    """
    return {"status": "success", "id": id}


@router.patch("/admin/{id}", dependencies=[Depends(require_auth)])
def admin_update_matching(id: int):
    """
    PATCH /matching/admin/{id}
    Middleware: auth:sanctum
    """
    return {"status": "success", "id": id}

