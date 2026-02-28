from fastapi import APIRouter, Depends

from app.core.dependencies import require_auth


router = APIRouter(tags=["social"])


@router.get("", dependencies=[Depends(require_auth)])
def list_social():
    return {"status": "success"}


@router.get("/profile/social/content-topics", dependencies=[Depends(require_auth)])
def profile_social_content_topics():
    return {"status": "success"}


@router.post("", dependencies=[Depends(require_auth)])
def create_social():
    return {"status": "success"}


@router.delete("/{id}", dependencies=[Depends(require_auth)])
def delete_social(id: int):
    return {"status": "success", "id": id}

