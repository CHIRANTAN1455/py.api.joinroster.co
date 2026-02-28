"""Matching endpoints. Laravel-exact: status, message, matching/creators. Path {id} = uuid, token as-is."""
from fastapi import APIRouter, Depends

from app.core.dependencies import require_auth
from app.core.laravel_response import success_with_message


router = APIRouter(prefix="/matching", tags=["matching"])


@router.get("", dependencies=[Depends(require_auth)])
def search_matching():
    return success_with_message("Matching Loaded Successfully", matching=[], total=0, page=1)


@router.get("/project/{id}", dependencies=[Depends(require_auth)])
def get_matching_project(id: str):
    return success_with_message("Matching Loaded Successfully", matching={})


@router.patch("/editor", dependencies=[Depends(require_auth)])
def update_matching_editor():
    return success_with_message("Matching updated", matching={})


@router.post("/public-matching")
def public_matching():
    return success_with_message("Matching created", matching={}, token=None)


@router.get("/{id}")
def get_matching(id: str):
    return success_with_message("Matching Loaded Successfully", matching={})


@router.get("/token/{token}")
def get_matching_by_token(token: str):
    return success_with_message("Matching Loaded Successfully", matching={})


@router.post("", dependencies=[Depends(require_auth)])
def create_matching():
    return success_with_message("Matching created", matching={}, token=None)


@router.post("/creators", dependencies=[Depends(require_auth)])
def matching_creators():
    return success_with_message("Creators Loaded Successfully", creators=[])


@router.patch("/{id}", dependencies=[Depends(require_auth)])
def update_matching(id: str):
    return success_with_message("Matching updated", matching={})


@router.patch("/admin/{id}", dependencies=[Depends(require_auth)])
def admin_update_matching(id: str):
    return success_with_message("Matching updated", matching={})
