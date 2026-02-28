"""User to-do. Path {id} = uuid. Laravel-exact: status, message, todo/todos."""
from fastapi import APIRouter, Depends

from app.core.dependencies import require_auth
from app.core.laravel_response import success_with_message


router = APIRouter(prefix="/user-to-do", tags=["user-to-do"])


@router.get("", dependencies=[Depends(require_auth)])
def list_user_todo():
    return success_with_message("To-dos Loaded Successfully", todos=[])


@router.post("", dependencies=[Depends(require_auth)])
def create_user_todo():
    return success_with_message("To-do Created Successfully", todo={})


@router.patch("/{id}", dependencies=[Depends(require_auth)])
def update_user_todo(id: str):
    return success_with_message("To-do Updated Successfully", todo={})


@router.delete("/{id}", dependencies=[Depends(require_auth)])
def delete_user_todo(id: str):
    return success_with_message("To-do Deleted Successfully")
