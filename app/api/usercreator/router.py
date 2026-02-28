"""UserCreator. Path {id} = uuid. Laravel-exact: status, message, creators/creator/projects/topics."""
from fastapi import APIRouter, Depends

from app.core.dependencies import require_auth
from app.core.laravel_response import success_with_message


router = APIRouter(prefix="/usercreator", tags=["usercreator"])


@router.get("", dependencies=[Depends(require_auth)])
def list_usercreators():
    return success_with_message("Creators Loaded Successfully", creators=[], total=0, page=1)


@router.get("/unverified", dependencies=[Depends(require_auth)])
def list_unverified_usercreators():
    return success_with_message("Creators Loaded Successfully", creators=[])


@router.get("/content-topics", dependencies=[Depends(require_auth)])
def usercreator_content_topics():
    return success_with_message("Content Topics Loaded Successfully", topics=[])


@router.get("/search", dependencies=[Depends(require_auth)])
def usercreator_search():
    return success_with_message("Creators Loaded Successfully", creators=[])


@router.get("/similar", dependencies=[Depends(require_auth)])
def usercreator_similar():
    return success_with_message("Creators Loaded Successfully", creators=[])


@router.post("", dependencies=[Depends(require_auth)])
def create_usercreator():
    return success_with_message("Creator Created Successfully", creator={})


@router.get("/info", dependencies=[Depends(require_auth)])
def usercreator_info():
    return success_with_message("Creator Loaded Successfully", creator={}, information=None)


@router.get("/{id}/projects", dependencies=[Depends(require_auth)])
def usercreator_projects(id: str):
    return success_with_message("Projects Loaded Successfully", projects=[])


@router.post("/{id}/update", dependencies=[Depends(require_auth)])
def update_usercreator(id: str):
    return success_with_message("Creator Updated Successfully", creator={})


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
def usercreator_search_public():
    return success_with_message("Creators Loaded Successfully", creators=[])


@router.get("/public/{username}")
def usercreator_public_username(username: str):
    return success_with_message("Creator Loaded Successfully", creator={}, creator_group=None)
