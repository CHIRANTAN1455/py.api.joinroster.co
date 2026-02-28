"""Path {id} = uuid. Laravel-exact: status, message, questionnaire."""
from fastapi import APIRouter

from app.core.laravel_response import success_with_message


router = APIRouter(prefix="/questionnaire", tags=["questionnaire"])


@router.get("/{id}")
def get_questionnaire(id: str):
    return success_with_message("Questionnaire Loaded Successfully", questionnaire={})


@router.post("/add")
def add_questionnaire():
    return success_with_message("Questionnaire response submitted", questionnaire={})
