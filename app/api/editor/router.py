"""Editor. Path {id} = uuid. Laravel-exact: status, message, editor/editors/projects/creators/etc."""
from fastapi import APIRouter, Depends

from app.core.dependencies import unlimited_rate
from app.core.laravel_response import success_with_message


router = APIRouter(prefix="/editor", tags=["editor"])


@router.api_route("", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
def editor_any():
    return success_with_message("Editor Loaded Successfully", editor={})


@router.get("/{id}")
def editor_get(id: str):
    return success_with_message("Editor Loaded Successfully", editor={})


@router.get("/metadata/{id}")
def editor_metadata(id: str):
    return success_with_message("Editor Loaded Successfully", editor={})


@router.get("/{id}/projects")
def editor_projects(id: str):
    return success_with_message("Projects Loaded Successfully", projects=[])


@router.get("/{id}/creators")
def editor_creators(id: str):
    return success_with_message("Creators Loaded Successfully", creators=[])


@router.get("/{id}/jobtypes")
def editor_jobtypes(id: str):
    return success_with_message("Job Types Loaded Successfully", job_types=[])


@router.get("/{id}/reviews")
def editor_reviews(id: str):
    return success_with_message("Reviews Loaded Successfully", reviews=[])


@router.post("/store")
def editor_store():
    return success_with_message("Editor Created Successfully", editor={})


@router.post("/admin/reset-password")
def editor_admin_reset_password():
    return success_with_message("Password reset sent")


@router.post("/email/{id}")
def editor_email(id: str):
    return success_with_message("Email sent")


@router.post("/profile/bulk-email/{id}", dependencies=[Depends(unlimited_rate)])
def editor_profile_bulk_email(id: str):
    return success_with_message("Emails sent")


@router.get("/{id}/related")
def editor_related(id: str):
    return success_with_message("Related Loaded Successfully", editors=[])
