from fastapi import APIRouter, Depends

from app.core.dependencies import require_auth


router = APIRouter(prefix="/usercreator", tags=["usercreator"])


@router.get("", dependencies=[Depends(require_auth)])
def list_usercreators():
    return {"status": "success"}


@router.get("/unverified", dependencies=[Depends(require_auth)])
def list_unverified_usercreators():
    return {"status": "success"}


@router.get("/content-topics", dependencies=[Depends(require_auth)])
def usercreator_content_topics():
    return {"status": "success"}


@router.get("/search", dependencies=[Depends(require_auth)])
def usercreator_search():
    return {"status": "success"}


@router.get("/similar", dependencies=[Depends(require_auth)])
def usercreator_similar():
    return {"status": "success"}


@router.post("", dependencies=[Depends(require_auth)])
def create_usercreator():
    return {"status": "success"}


@router.get("/info", dependencies=[Depends(require_auth)])
def usercreator_info():
    return {"status": "success"}


@router.get("/{id}/projects", dependencies=[Depends(require_auth)])
def usercreator_projects(id: int):
    return {"status": "success", "id": id}


@router.post("/{id}/update", dependencies=[Depends(require_auth)])
def update_usercreator(id: int):
    return {"status": "success", "id": id}


@router.delete("/{id}", dependencies=[Depends(require_auth)])
def delete_usercreator(id: int):
    return {"status": "success", "id": id}


@router.post("/colleauges/invite", dependencies=[Depends(require_auth)])
def usercreator_colleagues_invite():
    return {"status": "success"}


@router.post("/group/add")
def usercreator_group_add():
    return {"status": "success"}


@router.get("/public/info")
def usercreator_public_info():
    return {"status": "success"}


@router.get("/search/public")
def usercreator_search_public():
    return {"status": "success"}


@router.get("/public/{username}")
def usercreator_public_username(username: str):
    return {"status": "success", "username": username}

