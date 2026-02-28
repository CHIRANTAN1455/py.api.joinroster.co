"""Questionnaire and response."""
from datetime import datetime
from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

from app.db.models.questionnaire import Questionnaire, QuestionnaireResponse


def _questionnaire_resource(q: Questionnaire) -> Dict[str, Any]:
    return {"uuid": q.uuid, "title": q.title, "created_at": q.created_at}


class QuestionnaireService:
    def __init__(self, db: Session):
        self.db = db

    def get(self, uuid: str) -> Optional[Dict[str, Any]]:
        try:
            q = self.db.query(Questionnaire).filter(Questionnaire.uuid == uuid).first()
            return _questionnaire_resource(q) if q else None
        except Exception:
            return None

    def add_response(self, questionnaire_uuid: str, user_id: Optional[int], payload: Any) -> Optional[Dict[str, Any]]:
        try:
            q = self.db.query(Questionnaire).filter(Questionnaire.uuid == questionnaire_uuid).first()
            if not q:
                return None
            answers = str(payload) if payload else "{}"
            if isinstance(payload, dict):
                import json
                answers = json.dumps(payload)
            r = QuestionnaireResponse(questionnaire_id=q.id, user_id=user_id, answers=answers, created_at=datetime.utcnow(), updated_at=datetime.utcnow())
            self.db.add(r)
            self.db.commit()
            return _questionnaire_resource(q)
        except Exception:
            return None
