"""Social endpoints. Path {id} = uuid. Laravel-exact: status, message, social/socials. Mounted with prefix /api."""
from fastapi import APIRouter, Depends

from app.core.dependencies import require_auth
from app.core.laravel_response import success_with_message


router = APIRouter(prefix="", tags=["social"])


@router.get("/social", dependencies=[Depends(require_auth)])
def list_social():
    return success_with_message("Social Loaded Successfully", social=[])


@router.get("/profile/social/content-topics", dependencies=[Depends(require_auth)])
def profile_social_content_topics():
    return success_with_message("Content Topics Loaded Successfully", topics=[])


@router.post("/social", dependencies=[Depends(require_auth)])
def create_social():
    return success_with_message("Social Created Successfully", social={})


@router.delete("/social/{id}", dependencies=[Depends(require_auth)])
def delete_social(id: str):
    return success_with_message("Social Deleted Successfully")
