from fastapi import APIRouter, Depends

from app.core.dependencies import require_auth


router = APIRouter(prefix="/payment", tags=["payment"])


@router.get("", dependencies=[Depends(require_auth)])
def list_payments():
    return {"status": "success"}


@router.post("", dependencies=[Depends(require_auth)])
def create_payment():
    return {"status": "success"}


@router.delete("/{id}", dependencies=[Depends(require_auth)])
def delete_payment(id: int):
    return {"status": "success", "id": id}

