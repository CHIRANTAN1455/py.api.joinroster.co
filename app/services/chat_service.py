"""Chat: conversations and messages."""
import uuid as uuid_lib
from datetime import datetime
from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

from app.db.models.conversation import Conversation, Message
from app.db.models.project import Project
from app.db.models.user import User


def _message_resource(msg: Message, user: Optional[User] = None) -> Dict[str, Any]:
    return {
        "uuid": msg.uuid,
        "body": msg.body,
        "user": {"uuid": user.uuid, "name": user.name} if user else None,
        "created_at": msg.created_at,
    }


def _conversation_resource(conv: Conversation, project: Optional[Project] = None, messages: Optional[List] = None) -> Dict[str, Any]:
    return {
        "uuid": conv.uuid,
        "project": {"uuid": project.uuid, "title": project.title} if project else None,
        "messages": messages or [],
        "created_at": conv.created_at,
    }


class ChatService:
    def __init__(self, db: Session):
        self.db = db

    def list_conversations(self, user_id: int) -> List[Dict[str, Any]]:
        try:
            convs = self.db.query(Conversation).limit(50).all()
            out = []
            for c in convs:
                proj = self.db.query(Project).filter(Project.id == c.project_id).first() if c.project_id else None
                out.append(_conversation_resource(c, proj, []))
            return out
        except Exception:
            return []

    def get_conversation(self, uuid: str, user_id: int) -> Optional[Dict[str, Any]]:
        try:
            conv = self.db.query(Conversation).filter(Conversation.uuid == uuid).first()
            if not conv:
                return None
            proj = self.db.query(Project).filter(Project.id == conv.project_id).first() if conv.project_id else None
            msgs = self.db.query(Message).filter(Message.conversation_id == conv.id).order_by(Message.created_at).all()
            msg_list = []
            for m in msgs:
                u = self.db.query(User).filter(User.id == m.user_id).first()
                msg_list.append(_message_resource(m, u))
            return _conversation_resource(conv, proj, msg_list)
        except Exception:
            return None

    def get_received_messages(self, user_id: int) -> List[Dict[str, Any]]:
        try:
            msgs = self.db.query(Message).filter(Message.user_id != user_id).order_by(Message.created_at.desc()).limit(50).all()
            return [_message_resource(m, self.db.query(User).filter(User.id == m.user_id).first()) for m in msgs]
        except Exception:
            return []

    def init_conversation(self, user_id: int, project_uuid: Optional[str] = None) -> Optional[Dict[str, Any]]:
        try:
            project_id = None
            if project_uuid:
                p = self.db.query(Project).filter(Project.uuid == project_uuid).first()
                if p:
                    project_id = p.id
            conv = Conversation(
                uuid=str(uuid_lib.uuid4()),
                project_id=project_id,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            self.db.add(conv)
            self.db.commit()
            self.db.refresh(conv)
            proj = self.db.query(Project).filter(Project.id == conv.project_id).first() if conv.project_id else None
            return _conversation_resource(conv, proj, [])
        except Exception:
            return None

    def add_message(self, conversation_uuid: str, user_id: int, body: str) -> Optional[Dict[str, Any]]:
        try:
            conv = self.db.query(Conversation).filter(Conversation.uuid == conversation_uuid).first()
            if not conv:
                return None
            msg = Message(
                uuid=str(uuid_lib.uuid4()),
                conversation_id=conv.id,
                user_id=user_id,
                body=body,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            self.db.add(msg)
            self.db.commit()
            self.db.refresh(msg)
            u = self.db.query(User).filter(User.id == user_id).first()
            return _message_resource(msg, u)
        except Exception:
            return None

    def update_message(self, message_uuid: str, user_id: int, body: str) -> Optional[Dict[str, Any]]:
        try:
            msg = self.db.query(Message).filter(Message.uuid == message_uuid, Message.user_id == user_id).first()
            if not msg:
                return None
            msg.body = body
            msg.updated_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(msg)
            u = self.db.query(User).filter(User.id == user_id).first()
            return _message_resource(msg, u)
        except Exception:
            return None
