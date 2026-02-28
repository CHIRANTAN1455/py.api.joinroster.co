from fastapi import APIRouter, Depends

from app.core.dependencies import require_auth


router = APIRouter(prefix="/user-to-do", tags=["user-to-do"])


@router.get("", dependencies=[Depends(require_auth)])
def list_user_todo():
    return {"status": "success"}


@router.post("", dependencies=[Depends(require_auth)])
def create_user_todo():
    return {"status": "success"}


@router.patch("/{id}", dependencies=[Depends(require_auth)])
def update_user_todo(id: int):
    return {"status": "success", "id": id}


@router.delete("/{id}", dependencies=[Depends(require_auth)])
def delete_user_todo(id: int):
    return {"status": "success", "id": id}

