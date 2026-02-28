from fastapi import APIRouter


router = APIRouter(prefix="/questionnaire", tags=["questionnaire"])


@router.get("/{id}")
def get_questionnaire(id: int):
    return {"status": "success", "id": id}


@router.post("/add")
def add_questionnaire():
    return {"status": "success"}

