from fastapi import APIRouter, Depends

from app.core.dependencies import require_auth


router = APIRouter(prefix="/chat", tags=["chat"])


@router.get("", dependencies=[Depends(require_auth)])
def list_chats():
    """
    GET /chat
    Middleware: auth:sanctum
    """
    return {"status": "success"}


@router.get("/received_messages", dependencies=[Depends(require_auth)])
def get_received_messages():
    """
    GET /chat/received_messages
    Middleware: auth:sanctum
    """
    return {"status": "success"}


@router.post("/init/public", dependencies=[Depends(require_auth)])
def init_public_chat():
    """
    POST /chat/init/public
    Middleware: auth:sanctum
    """
    return {"status": "success"}


@router.post("/init", dependencies=[Depends(require_auth)])
def init_chat():
    """
    POST /chat/init
    Middleware: auth:sanctum
    """
    return {"status": "success"}


@router.get("/{id}", dependencies=[Depends(require_auth)])
def get_chat(id: int):
    """
    GET /chat/{id}
    Middleware: auth:sanctum
    """
    return {"status": "success", "id": id}


@router.post("/{id}", dependencies=[Depends(require_auth)])
def post_chat_message(id: int):
    """
    POST /chat/{id}
    Middleware: auth:sanctum
    """
    return {"status": "success", "id": id}


@router.post("/admin/custom", dependencies=[Depends(require_auth)])
def admin_custom_message():
    """
    POST /chat/admin/custom
    Middleware: auth:sanctum
    """
    return {"status": "success"}


@router.patch("/message/{id}", dependencies=[Depends(require_auth)])
def update_message(id: int):
    """
    PATCH /chat/message/{id}
    Middleware: auth:sanctum
    """
    return {"status": "success", "id": id}

