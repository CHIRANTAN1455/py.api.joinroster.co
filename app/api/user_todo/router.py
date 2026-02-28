"""User to-do. Path {id} = uuid. Laravel-exact: status, message, todo/todos."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user_id, require_auth
from app.core.laravel_response import success_with_message
from app.db.session import get_db
from app.services.user_todo_service import UserTodoService


router = APIRouter(prefix="/user-to-do", tags=["user-to-do"])


def get_todo_service(db: Session = Depends(get_db)) -> UserTodoService:
    return UserTodoService(db=db)


@router.get("", dependencies=[Depends(require_auth)])
def list_user_todo(
    service: UserTodoService = Depends(get_todo_service),
    current_user_id: int = Depends(get_current_user_id),
):
    todos = service.list(current_user_id)
    return success_with_message("To-dos Loaded Successfully", todos=todos)


@router.post("", dependencies=[Depends(require_auth)])
def create_user_todo(
    body: dict = None,
    service: UserTodoService = Depends(get_todo_service),
    current_user_id: int = Depends(get_current_user_id),
):
    todo = service.create(current_user_id, body or {})
    return success_with_message("To-do Created Successfully", todo=todo or {})


@router.patch("/{id}", dependencies=[Depends(require_auth)])
def update_user_todo(
    id: str,
    body: dict = None,
    service: UserTodoService = Depends(get_todo_service),
    current_user_id: int = Depends(get_current_user_id),
):
    todo = service.update(id, current_user_id, body or {})
    if not todo:
        return {"status": "error", "todo": {}}
    return success_with_message("To-do Updated Successfully", todo=todo)


@router.delete("/{id}", dependencies=[Depends(require_auth)])
def delete_user_todo(
    id: str,
    service: UserTodoService = Depends(get_todo_service),
    current_user_id: int = Depends(get_current_user_id),
):
    ok = service.delete(id, current_user_id)
    if not ok:
        return {"status": "error", "message": "To-do not found"}
    return success_with_message("To-do Deleted Successfully")
