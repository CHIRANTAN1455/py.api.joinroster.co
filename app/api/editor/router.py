"""Editor. Path {id} = uuid. Laravel-exact: status, message, editor/editors/projects/creators/etc."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.dependencies import unlimited_rate
from app.core.laravel_response import success_with_message
from app.db.session import get_db
from app.services.editor_service import EditorService


router = APIRouter(prefix="/editor", tags=["editor"])


def get_editor_service(db: Session = Depends(get_db)) -> EditorService:
    return EditorService(db=db)


@router.api_route("", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
def editor_any(service: EditorService = Depends(get_editor_service)):
    return success_with_message("Editor Loaded Successfully", editor={})


@router.get("/{id}")
def editor_get(id: str, service: EditorService = Depends(get_editor_service)):
    editor = service.get_editor(id)
    if not editor:
        return {"status": "error", "message": "Editor not found", "editor": {}}
    return success_with_message("Editor Loaded Successfully", editor=editor)


@router.get("/metadata/{id}")
def editor_metadata(id: str, service: EditorService = Depends(get_editor_service)):
    editor = service.get_editor(id)
    if not editor:
        return {"status": "error", "message": "Editor not found", "editor": {}}
    return success_with_message("Editor Loaded Successfully", editor=editor)


@router.get("/{id}/projects")
def editor_projects(
    id: str,
    page: int = Query(1, ge=1),
    service: EditorService = Depends(get_editor_service),
):
    result = service.get_projects(id, page=page)
    return success_with_message(
        "Projects Loaded Successfully",
        projects=result["projects"],
        total=result["total"],
        page=result["page"],
    )


@router.get("/{id}/creators")
def editor_creators(id: str, service: EditorService = Depends(get_editor_service)):
    creators = service.get_creators(id)
    return success_with_message("Creators Loaded Successfully", creators=creators)


@router.get("/{id}/jobtypes")
def editor_jobtypes(id: str, service: EditorService = Depends(get_editor_service)):
    job_types = service.get_jobtypes(id)
    return success_with_message("Job Types Loaded Successfully", job_types=job_types)


@router.get("/{id}/reviews")
def editor_reviews(id: str, service: EditorService = Depends(get_editor_service)):
    reviews = service.get_reviews(id)
    return success_with_message("Reviews Loaded Successfully", reviews=reviews)


@router.post("/store")
def editor_store(service: EditorService = Depends(get_editor_service)):
    return success_with_message("Editor Created Successfully", editor={})


@router.post("/admin/reset-password")
def editor_admin_reset_password(service: EditorService = Depends(get_editor_service)):
    return success_with_message("Password reset sent")


@router.post("/email/{id}")
def editor_email(id: str, service: EditorService = Depends(get_editor_service)):
    return success_with_message("Email sent")


@router.post("/profile/bulk-email/{id}", dependencies=[Depends(unlimited_rate)])
def editor_profile_bulk_email(id: str, service: EditorService = Depends(get_editor_service)):
    return success_with_message("Emails sent")


@router.get("/{id}/related")
def editor_related(id: str, service: EditorService = Depends(get_editor_service)):
    editors = service.get_related(id)
    return success_with_message("Related Loaded Successfully", editors=editors)
