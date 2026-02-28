from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import lenient_rate_limit
from app.core.laravel_response import skill_to_laravel_skill_resource
from app.db.models.skill import Skill
from app.db.session import get_db


router = APIRouter(prefix="", tags=["lookups"])


@router.get("/skills", dependencies=[Depends(lenient_rate_limit)])
def skills(db: Session = Depends(get_db)) -> dict:
    """
    GET /skills

    Laravel SkillController@index:
    returns api(['status', 'message', 'skills' => SkillResource::collection(...)])
    """
    # Filter to active + not hidden skills, mirroring Laravel SkillController.
    query = db.query(Skill).filter(Skill.active == 1, Skill.hide_from_customers == 0)
    skills_rows: List[Skill] = query.order_by(Skill.name.asc()).all()
    return {
        "status": "success",
        "message": "Skills Loaded Successfully",
        "skills": [skill_to_laravel_skill_resource(s) for s in skills_rows],
    }


@router.get("/skills/get", dependencies=[Depends(lenient_rate_limit)])
def skills_get():
    return {"status": "success"}


@router.get("/contentverticals", dependencies=[Depends(lenient_rate_limit)])
def contentverticals():
    return {"status": "success"}


@router.get("/contentverticals/get", dependencies=[Depends(lenient_rate_limit)])
def contentverticals_get():
    return {"status": "success"}


@router.get("/platforms", dependencies=[Depends(lenient_rate_limit)])
def platforms():
    return {"status": "success"}


@router.get("/platforms/get", dependencies=[Depends(lenient_rate_limit)])
def platforms_get():
    return {"status": "success"}


@router.get("/softwares", dependencies=[Depends(lenient_rate_limit)])
def softwares():
    return {"status": "success"}


@router.get("/softwares/get", dependencies=[Depends(lenient_rate_limit)])
def softwares_get():
    return {"status": "success"}


@router.get("/equipments", dependencies=[Depends(lenient_rate_limit)])
def equipments():
    return {"status": "success"}


@router.get("/equipments/get", dependencies=[Depends(lenient_rate_limit)])
def equipments_get():
    return {"status": "success"}


@router.get("/creativestyles", dependencies=[Depends(lenient_rate_limit)])
def creativestyles():
    return {"status": "success"}


@router.get("/creativestyles/get", dependencies=[Depends(lenient_rate_limit)])
def creativestyles_get():
    return {"status": "success"}


@router.get("/contentforms", dependencies=[Depends(lenient_rate_limit)])
def contentforms():
    return {"status": "success"}


@router.get("/contentforms/get", dependencies=[Depends(lenient_rate_limit)])
def contentforms_get():
    return {"status": "success"}


@router.get("/projecttypes", dependencies=[Depends(lenient_rate_limit)])
def projecttypes():
    return {"status": "success"}


@router.get("/projecttypes/{username}", dependencies=[Depends(lenient_rate_limit)])
def projecttypes_username(username: str):
    return {"status": "success", "username": username}


@router.get("/projecttypes/get", dependencies=[Depends(lenient_rate_limit)])
def projecttypes_get():
    return {"status": "success"}


@router.get("/jobtypes", dependencies=[Depends(lenient_rate_limit)])
def jobtypes():
    return {"status": "success"}


@router.get("/jobtypes/get", dependencies=[Depends(lenient_rate_limit)])
def jobtypes_get():
    return {"status": "success"}


@router.get("/reasons", dependencies=[Depends(lenient_rate_limit)])
def reasons():
    return {"status": "success"}


@router.get("/reasons/get", dependencies=[Depends(lenient_rate_limit)])
def reasons_get():
    return {"status": "success"}


@router.get("/referrals", dependencies=[Depends(lenient_rate_limit)])
def referrals():
    return {"status": "success"}


@router.get("/referrals/get", dependencies=[Depends(lenient_rate_limit)])
def referrals_get():
    return {"status": "success"}


@router.get("/location")
def location():
    return {"status": "success"}


@router.get("/location/{id}")
def location_id(id: int):
    return {"status": "success", "id": id}

