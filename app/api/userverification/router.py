from fastapi import APIRouter, Depends

from app.core.dependencies import require_auth


router = APIRouter(prefix="/userverification", tags=["userverification"])


@router.get("", dependencies=[Depends(require_auth)])
def list_userverification():
    return {"status": "success"}


@router.post("", dependencies=[Depends(require_auth)])
def create_userverification():
    return {"status": "success"}


@router.post("/many", dependencies=[Depends(require_auth)])
def create_many_userverification():
    return {"status": "success"}


@router.delete("/{id}", dependencies=[Depends(require_auth)])
def delete_userverification(id: int):
    return {"status": "success", "id": id}

