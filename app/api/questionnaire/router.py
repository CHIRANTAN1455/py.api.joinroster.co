"""Path {id} = uuid. Laravel-exact: status, message, questionnaire."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.laravel_response import success_with_message
from app.db.session import get_db
from app.services.questionnaire_service import QuestionnaireService


router = APIRouter(prefix="/questionnaire", tags=["questionnaire"])


def get_questionnaire_service(db: Session = Depends(get_db)) -> QuestionnaireService:
    return QuestionnaireService(db=db)


@router.get("/{id}")
def get_questionnaire(id: str, service: QuestionnaireService = Depends(get_questionnaire_service)):
    questionnaire = service.get(id)
    if not questionnaire:
        return {"status": "error", "questionnaire": {}}
    return success_with_message("Questionnaire Loaded Successfully", questionnaire=questionnaire)


@router.post("/add")
def add_questionnaire(
    body: dict = None,
    service: QuestionnaireService = Depends(get_questionnaire_service),
):
    quuid = body.get("questionnaire_uuid", "") if body else ""
    questionnaire = service.add_response(quuid, None, body)
    if not questionnaire:
        return {"status": "error", "questionnaire": {}}
    return success_with_message("Questionnaire response submitted", questionnaire=questionnaire)
