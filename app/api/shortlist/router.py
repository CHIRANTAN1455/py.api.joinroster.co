from fastapi import APIRouter, Depends

from app.core.dependencies import require_auth


router = APIRouter(prefix="/shortlist", tags=["shortlist"])


@router.get("", dependencies=[Depends(require_auth)])
def list_shortlist():
    return {"status": "success"}


@router.patch("/{id}", dependencies=[Depends(require_auth)])
def update_shortlist(id: int):
    return {"status": "success", "id": id}


@router.delete("/{id}", dependencies=[Depends(require_auth)])
def delete_shortlist(id: int):
    return {"status": "success", "id": id}

