"""UserProject. Path {id} = uuid. Laravel-exact: status, message, project/projects/info."""
from fastapi import APIRouter, Depends

from app.core.dependencies import require_auth
from app.core.laravel_response import success_with_message


router = APIRouter(prefix="/userproject", tags=["userproject"])


@router.get("/public/info")
def userproject_public_info():
    return success_with_message("Info Loaded Successfully", info={})


@router.get("/public")
def userproject_public():
    return success_with_message("Projects Loaded Successfully", projects=[], total=0, page=1)


@router.get("", dependencies=[Depends(require_auth)])
def list_userprojects():
    return success_with_message("Projects Loaded Successfully", projects=[], total=0, page=1)


@router.get("/info", dependencies=[Depends(require_auth)])
def userproject_info():
    return success_with_message("Info Loaded Successfully", info={})


@router.post("", dependencies=[Depends(require_auth)])
def create_userproject():
    return success_with_message("Project Created Successfully", project={})


@router.post("/{id}/update", dependencies=[Depends(require_auth)])
def update_userproject(id: str):
    return success_with_message("Project Updated Successfully", project={})


@router.delete("/{id}", dependencies=[Depends(require_auth)])
def delete_userproject(id: str):
    return success_with_message("Project Deleted Successfully")
