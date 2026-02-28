"""Project screening questions CRUD."""
import uuid as uuid_lib
from datetime import datetime
from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

from app.db.models.project import Project
from app.db.models.project_screening_question import ProjectScreeningQuestion


def _question_resource(q: ProjectScreeningQuestion) -> Dict[str, Any]:
    return {"uuid": q.uuid, "question": q.question, "order": q.order, "created_at": q.created_at}


class ProjectScreeningService:
    def __init__(self, db: Session):
        self.db = db

    def list(self, project_uuid: str) -> List[Dict[str, Any]]:
        try:
            proj = self.db.query(Project).filter(Project.uuid == project_uuid).first()
            if not proj:
                return []
            items = self.db.query(ProjectScreeningQuestion).filter(ProjectScreeningQuestion.project_id == proj.id).order_by(ProjectScreeningQuestion.order).all()
            return [_question_resource(q) for q in items]
        except Exception:
            return []

    def get(self, project_uuid: str, question_uuid: str) -> Optional[Dict[str, Any]]:
        try:
            proj = self.db.query(Project).filter(Project.uuid == project_uuid).first()
            if not proj:
                return None
            q = self.db.query(ProjectScreeningQuestion).filter(ProjectScreeningQuestion.project_id == proj.id, ProjectScreeningQuestion.uuid == question_uuid).first()
            return _question_resource(q) if q else None
        except Exception:
            return None

    def create(self, project_uuid: str, payload: Any) -> Optional[Dict[str, Any]]:
        try:
            proj = self.db.query(Project).filter(Project.uuid == project_uuid).first()
            if not proj:
                return None
            question = payload.get("question", "") if isinstance(payload, dict) else getattr(payload, "question", "")
            q = ProjectScreeningQuestion(uuid=str(uuid_lib.uuid4()), project_id=proj.id, question=question, order=0, created_at=datetime.utcnow(), updated_at=datetime.utcnow())
            self.db.add(q)
            self.db.commit()
            self.db.refresh(q)
            return _question_resource(q)
        except Exception:
            return None

    def update(self, project_uuid: str, question_uuid: str, payload: Any) -> Optional[Dict[str, Any]]:
        try:
            proj = self.db.query(Project).filter(Project.uuid == project_uuid).first()
            if not proj:
                return None
            q = self.db.query(ProjectScreeningQuestion).filter(ProjectScreeningQuestion.project_id == proj.id, ProjectScreeningQuestion.uuid == question_uuid).first()
            if not q:
                return None
            if isinstance(payload, dict) and "question" in payload:
                q.question = payload["question"]
            q.updated_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(q)
            return _question_resource(q)
        except Exception:
            return None

    def delete(self, project_uuid: str, question_uuid: str) -> bool:
        try:
            proj = self.db.query(Project).filter(Project.uuid == project_uuid).first()
            if not proj:
                return False
            q = self.db.query(ProjectScreeningQuestion).filter(ProjectScreeningQuestion.project_id == proj.id, ProjectScreeningQuestion.uuid == question_uuid).first()
            if not q:
                return False
            self.db.delete(q)
            self.db.commit()
            return True
        except Exception:
            return False
