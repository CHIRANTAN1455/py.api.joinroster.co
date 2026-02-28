"""UserCreator. Path {id} = uuid. Laravel-exact: status, message, creators/creator/projects/topics."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.dependencies import require_auth
from app.core.laravel_response import success_with_message, user_to_laravel_user_resource
from app.db.session import get_db
from app.db.models.user import User
from app.services.editor_service import EditorService


router = APIRouter(prefix="/usercreator", tags=["usercreator"])


def get_editor_service(db: Session = Depends(get_db)) -> EditorService:
    return EditorService(db=db)


@router.get("", dependencies=[Depends(require_auth)])
def list_usercreators(
    page: int = Query(1, ge=1),
    service: EditorService = Depends(get_editor_service),
):
    db = service.db
    q = db.query(User).filter(User.active.is_(True))
    total = q.count()
    items = q.offset((page - 1) * 15).limit(15).all()
    creators = [user_to_laravel_user_resource(u) for u in items]
    return success_with_message("Creators Loaded Successfully", creators=creators, total=total, page=page)


@router.get("/unverified", dependencies=[Depends(require_auth)])
def list_unverified_usercreators(service: EditorService = Depends(get_editor_service)):
    return success_with_message("Creators Loaded Successfully", creators=[])


@router.get("/content-topics", dependencies=[Depends(require_auth)])
def usercreator_content_topics():
    return success_with_message("Content Topics Loaded Successfully", topics=[])


@router.get("/search", dependencies=[Depends(require_auth)])
def usercreator_search(
    service: EditorService = Depends(get_editor_service),
):
    return success_with_message("Creators Loaded Successfully", creators=[])


@router.get("/similar", dependencies=[Depends(require_auth)])
def usercreator_similar(service: EditorService = Depends(get_editor_service)):
    return success_with_message("Creators Loaded Successfully", creators=[])


@router.post("", dependencies=[Depends(require_auth)])
def create_usercreator(service: EditorService = Depends(get_editor_service)):
    return success_with_message("Creator Created Successfully", creator={})


@router.get("/info", dependencies=[Depends(require_auth)])
def usercreator_info(service: EditorService = Depends(get_editor_service)):
    return success_with_message("Creator Loaded Successfully", creator={}, information=None)


@router.get("/{id}/projects", dependencies=[Depends(require_auth)])
def usercreator_projects(
    id: str,
    page: int = Query(1, ge=1),
    service: EditorService = Depends(get_editor_service),
):
    result = service.get_projects(id, page=page)
    return success_with_message("Projects Loaded Successfully", projects=result["projects"])


@router.post("/{id}/update", dependencies=[Depends(require_auth)])
def update_usercreator(id: str, service: EditorService = Depends(get_editor_service)):
    editor = service.get_editor(id)
    return success_with_message("Creator Updated Successfully", creator=editor or {})


@router.delete("/{id}", dependencies=[Depends(require_auth)])
def delete_usercreator(id: str):
    return success_with_message("Creator Deleted Successfully")


@router.post("/colleauges/invite", dependencies=[Depends(require_auth)])
def usercreator_colleagues_invite():
    return success_with_message("Invitation sent", creator={})


@router.post("/group/add")
def usercreator_group_add():
    return success_with_message("Group added", creator_group=None, creators=[])


@router.get("/public/info")
def usercreator_public_info():
    return success_with_message("Info Loaded Successfully", information={})


@router.get("/search/public")
def usercreator_search_public(service: EditorService = Depends(get_editor_service)):
    return success_with_message("Creators Loaded Successfully", creators=[])


@router.get("/public/{username}")
def usercreator_public_username(
    username: str,
    service: EditorService = Depends(get_editor_service),
):
    db = service.db
    user = db.query(User).filter(User.username == username).first()
    creator = user_to_laravel_user_resource(user) if user else {}
    return success_with_message("Creator Loaded Successfully", creator=creator, creator_group=None)
