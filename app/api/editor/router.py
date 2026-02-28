from fastapi import APIRouter, Depends

from app.core.dependencies import unlimited_rate


router = APIRouter(prefix="/editor", tags=["editor"])


@router.api_route("", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
def editor_any():
    """
    ANY /editor
    Middleware: none
    """
    return {"status": "success"}


@router.get("/{id}")
def editor_get(id: int):
    return {"status": "success", "id": id}


@router.get("/metadata/{id}")
def editor_metadata(id: int):
    return {"status": "success", "id": id}


@router.get("/{id}/projects")
def editor_projects(id: int):
    return {"status": "success", "id": id}


@router.get("/{id}/creators")
def editor_creators(id: int):
    return {"status": "success", "id": id}


@router.get("/{id}/jobtypes")
def editor_jobtypes(id: int):
    return {"status": "success", "id": id}


@router.get("/{id}/reviews")
def editor_reviews(id: int):
    return {"status": "success", "id": id}


@router.post("/store")
def editor_store():
    return {"status": "success"}


@router.post("/admin/reset-password")
def editor_admin_reset_password():
    return {"status": "success"}


@router.post("/email/{id}")
def editor_email(id: int):
    return {"status": "success", "id": id}


@router.post(
    "/profile/bulk-email/{id}",
    dependencies=[Depends(unlimited_rate)],
)
def editor_profile_bulk_email(id: int):
    return {"status": "success", "id": id}


@router.get("/{id}/related")
def editor_related(id: int):
    return {"status": "success", "id": id}

