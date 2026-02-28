"""Shortlist. Path {id} = uuid. Laravel-exact: status, message, shortlist/shortlists."""
from fastapi import APIRouter, Depends

from app.core.dependencies import require_auth
from app.core.laravel_response import success_with_message


router = APIRouter(prefix="/shortlist", tags=["shortlist"])


@router.get("", dependencies=[Depends(require_auth)])
def list_shortlist():
    return success_with_message("Shortlist Loaded Successfully", shortlist=[])


@router.patch("/{id}", dependencies=[Depends(require_auth)])
def update_shortlist(id: str):
    return success_with_message("Shortlist Updated Successfully", shortlist={})


@router.delete("/{id}", dependencies=[Depends(require_auth)])
def delete_shortlist(id: str):
    return success_with_message("Shortlist Deleted Successfully")
