"""Chat endpoints. Laravel-exact: status, message, chat/conversation/messages. Path {id} = uuid."""
from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user_id, require_auth
from app.core.laravel_response import success_with_message
from app.db.session import get_db
from app.services.chat_service import ChatService


router = APIRouter(prefix="/chat", tags=["chat"])


def get_chat_service(db: Session = Depends(get_db)) -> ChatService:
    return ChatService(db=db)


@router.get("", dependencies=[Depends(require_auth)])
def list_chats(
    service: ChatService = Depends(get_chat_service),
    current_user_id: int = Depends(get_current_user_id),
):
    conversations = service.list_conversations(current_user_id)
    return success_with_message("Chat Loaded Successfully", chats=[], conversations=conversations)


@router.get("/received_messages", dependencies=[Depends(require_auth)])
def get_received_messages(
    service: ChatService = Depends(get_chat_service),
    current_user_id: int = Depends(get_current_user_id),
):
    messages = service.get_received_messages(current_user_id)
    return success_with_message("Messages Loaded Successfully", messages=messages)


@router.post("/init/public", dependencies=[Depends(require_auth)])
def init_public_chat(
    service: ChatService = Depends(get_chat_service),
    current_user_id: int = Depends(get_current_user_id),
):
    conv = service.init_conversation(current_user_id, None)
    return success_with_message("Chat initialized", conversation=conv)


@router.post("/init", dependencies=[Depends(require_auth)])
def init_chat(
    service: ChatService = Depends(get_chat_service),
    current_user_id: int = Depends(get_current_user_id),
):
    conv = service.init_conversation(current_user_id, None)
    return success_with_message("Chat initialized", conversation=conv)


@router.get("/{id}", dependencies=[Depends(require_auth)])
def get_chat(
    id: str,
    service: ChatService = Depends(get_chat_service),
    current_user_id: int = Depends(get_current_user_id),
):
    conv = service.get_conversation(id, current_user_id)
    if not conv:
        return {"status": "error", "chat": {}, "conversation": []}
    return success_with_message("Chat Loaded Successfully", chat=conv, conversation=conv.get("messages", []))


@router.post("/{id}", dependencies=[Depends(require_auth)])
def post_chat_message(
    id: str,
    body: Optional[dict] = None,
    service: ChatService = Depends(get_chat_service),
    current_user_id: int = Depends(get_current_user_id),
):
    msg_body = body.get("body", "") if isinstance(body, dict) else ""
    msg = service.add_message(id, current_user_id, msg_body)
    if not msg:
        return {"status": "error", "message": {}}
    return success_with_message("Message sent", message=msg)


@router.post("/admin/custom", dependencies=[Depends(require_auth)])
def admin_custom_message(service: ChatService = Depends(get_chat_service)):
    return success_with_message("Message sent")


@router.patch("/message/{id}", dependencies=[Depends(require_auth)])
def update_message(
    id: str,
    body: Optional[dict] = None,
    service: ChatService = Depends(get_chat_service),
    current_user_id: int = Depends(get_current_user_id),
):
    msg_body = body.get("body", "") if isinstance(body, dict) else ""
    msg = service.update_message(id, current_user_id, msg_body)
    if not msg:
        return {"status": "error", "message": {}}
    return success_with_message("Message updated", message=msg)
