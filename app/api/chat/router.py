"""Chat endpoints. Laravel-exact: status, message, chat/conversation/messages. Path {id} = uuid."""
from fastapi import APIRouter, Depends

from app.core.dependencies import require_auth
from app.core.laravel_response import success_with_message


router = APIRouter(prefix="/chat", tags=["chat"])


@router.get("", dependencies=[Depends(require_auth)])
def list_chats():
    return success_with_message("Chat Loaded Successfully", chats=[], conversations=[])


@router.get("/received_messages", dependencies=[Depends(require_auth)])
def get_received_messages():
    return success_with_message("Messages Loaded Successfully", messages=[])


@router.post("/init/public", dependencies=[Depends(require_auth)])
def init_public_chat():
    return success_with_message("Chat initialized", conversation=None)


@router.post("/init", dependencies=[Depends(require_auth)])
def init_chat():
    return success_with_message("Chat initialized", conversation=None)


@router.get("/{id}", dependencies=[Depends(require_auth)])
def get_chat(id: str):
    return success_with_message("Chat Loaded Successfully", chat={}, conversation=[])


@router.post("/{id}", dependencies=[Depends(require_auth)])
def post_chat_message(id: str):
    return success_with_message("Message sent", message={})


@router.post("/admin/custom", dependencies=[Depends(require_auth)])
def admin_custom_message():
    return success_with_message("Message sent")


@router.patch("/message/{id}", dependencies=[Depends(require_auth)])
def update_message(id: str):
    return success_with_message("Message updated", message={})
