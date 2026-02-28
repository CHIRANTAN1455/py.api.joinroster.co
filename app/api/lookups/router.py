"""
Lookups: skills, content_verticals, platforms, softwares, equipments,
creativestyles, contentforms, projecttypes, jobtypes, reasons, referrals, location.
Laravel-exact response: status, message, and collection key (same keys/casing as Laravel).
All resources output uuid only (no integer id).
"""
from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.dependencies import lenient_rate_limit
from app.core.laravel_response import (
    location_to_laravel_resource,
    lookup_to_laravel_resource,
    project_type_to_laravel_resource,
    reason_to_laravel_resource,
    referral_to_laravel_resource,
    skill_to_laravel_skill_resource,
)
from app.db.models.content_form import ContentForm
from app.db.models.content_vertical import ContentVertical
from app.db.models.creative_style import CreativeStyle
from app.db.models.equipment import Equipment
from app.db.models.job_type import JobType
from app.db.models.location import Location
from app.db.models.platform import Platform
from app.db.models.project_type import ProjectType
from app.db.models.reason import Reason
from app.db.models.referral import Referral
from app.db.models.skill import Skill
from app.db.models.software import Software
from app.db.session import get_db


router = APIRouter(prefix="", tags=["lookups"])


def _success_with_collection(
    message: str, key: str, items: list
) -> dict:
    """Laravel shape: status, message, <key>: [...]"""
    return {"status": "success", "message": message, key: items}


@router.get("/skills", dependencies=[Depends(lenient_rate_limit)])
def skills(db: Session = Depends(get_db)) -> dict:
    """GET /skills — status, message, skills (uuid, icon, name, description)."""
    rows = (
        db.query(Skill)
        .filter(Skill.active == 1, Skill.hide_from_customers == 0)
        .order_by(Skill.name.asc())
        .all()
    )
    return _success_with_collection(
        "Skills Loaded Successfully",
        "skills",
        [skill_to_laravel_skill_resource(s) for s in rows],
    )


@router.get("/skills/get", dependencies=[Depends(lenient_rate_limit)])
def skills_get(db: Session = Depends(get_db)) -> dict:
    """Same as /skills."""
    return skills(db=db)


@router.get("/contentverticals", dependencies=[Depends(lenient_rate_limit)])
def contentverticals(db: Session = Depends(get_db)) -> dict:
    """GET /contentverticals — status, message, content_verticals."""
    rows = (
        db.query(ContentVertical)
        .filter(ContentVertical.active == 1)
        .order_by(ContentVertical.name.asc())
        .all()
    )
    return _success_with_collection(
        "Content Verticals Loaded Successfully",
        "content_verticals",
        [lookup_to_laravel_resource(r) for r in rows],
    )


@router.get("/contentverticals/get", dependencies=[Depends(lenient_rate_limit)])
def contentverticals_get(db: Session = Depends(get_db)) -> dict:
    return contentverticals(db=db)


@router.get("/platforms", dependencies=[Depends(lenient_rate_limit)])
def platforms(db: Session = Depends(get_db)) -> dict:
    """GET /platforms — status, message, platforms."""
    rows = (
        db.query(Platform)
        .filter(Platform.active == 1, Platform.hide_from_customers == 0)
        .order_by(Platform.name.asc())
        .all()
    )
    return _success_with_collection(
        "Platforms Loaded Successfully",
        "platforms",
        [lookup_to_laravel_resource(r) for r in rows],
    )


@router.get("/platforms/get", dependencies=[Depends(lenient_rate_limit)])
def platforms_get(db: Session = Depends(get_db)) -> dict:
    return platforms(db=db)


@router.get("/softwares", dependencies=[Depends(lenient_rate_limit)])
def softwares(
    db: Session = Depends(get_db),
    search: Optional[str] = Query(None),
) -> dict:
    """GET /softwares — status, message, softwares."""
    q = db.query(Software).filter(Software.active == 1)
    if search:
        q = q.filter(Software.name.ilike(f"%{search}%"))
    rows = q.order_by(Software.name.asc()).all()
    return _success_with_collection(
        "Software Loaded Successfully",
        "softwares",
        [lookup_to_laravel_resource(r) for r in rows],
    )


@router.get("/softwares/get", dependencies=[Depends(lenient_rate_limit)])
def softwares_get(db: Session = Depends(get_db)) -> dict:
    return softwares(db=db)


@router.get("/equipments", dependencies=[Depends(lenient_rate_limit)])
def equipments(db: Session = Depends(get_db)) -> dict:
    """GET /equipments — status, message, equipments."""
    rows = (
        db.query(Equipment)
        .filter(Equipment.active == 1)
        .order_by(Equipment.name.asc())
        .all()
    )
    return _success_with_collection(
        "Equipment Loaded Successfully",
        "equipments",
        [lookup_to_laravel_resource(r) for r in rows],
    )


@router.get("/equipments/get", dependencies=[Depends(lenient_rate_limit)])
def equipments_get(db: Session = Depends(get_db)) -> dict:
    return equipments(db=db)


@router.get("/creativestyles", dependencies=[Depends(lenient_rate_limit)])
def creativestyles(db: Session = Depends(get_db)) -> dict:
    """GET /creativestyles — status, message, creative_styles."""
    rows = (
        db.query(CreativeStyle)
        .filter(CreativeStyle.active == 1, CreativeStyle.hide_from_customers == 0)
        .order_by(CreativeStyle.name.asc())
        .all()
    )
    return _success_with_collection(
        "Creative Styles Loaded Successfully",
        "creative_styles",
        [lookup_to_laravel_resource(r) for r in rows],
    )


@router.get("/creativestyles/get", dependencies=[Depends(lenient_rate_limit)])
def creativestyles_get(db: Session = Depends(get_db)) -> dict:
    return creativestyles(db=db)


@router.get("/contentforms", dependencies=[Depends(lenient_rate_limit)])
def contentforms(db: Session = Depends(get_db)) -> dict:
    """GET /contentforms — status, message, content_forms."""
    rows = (
        db.query(ContentForm)
        .filter(ContentForm.active == 1)
        .order_by(ContentForm.name.asc())
        .all()
    )
    return _success_with_collection(
        "Content Forms Loaded Successfully",
        "content_forms",
        [lookup_to_laravel_resource(r) for r in rows],
    )


@router.get("/contentforms/get", dependencies=[Depends(lenient_rate_limit)])
def contentforms_get(db: Session = Depends(get_db)) -> dict:
    return contentforms(db=db)


@router.get("/projecttypes", dependencies=[Depends(lenient_rate_limit)])
def projecttypes(
    db: Session = Depends(get_db),
    username: Optional[str] = None,
) -> dict:
    """GET /projecttypes — status, message, project_types. Optional username for user-scoped."""
    rows = (
        db.query(ProjectType)
        .filter(ProjectType.active == 1)
        .order_by(ProjectType.name.asc())
        .all()
    )
    # ProjectTypeResource has count; we don't have user context here, use 0
    out = [
        {**project_type_to_laravel_resource(r), "count": getattr(r, "count", 0)}
        for r in rows
    ]
    return _success_with_collection(
        "Project Types Loaded Successfully",
        "project_types",
        out,
    )


@router.get("/projecttypes/{username}", dependencies=[Depends(lenient_rate_limit)])
def projecttypes_username(
    username: str,
    db: Session = Depends(get_db),
) -> dict:
    """Same shape as projecttypes; username can be used for user-scoped types."""
    return projecttypes(db=db, username=username)


@router.get("/projecttypes/get", dependencies=[Depends(lenient_rate_limit)])
def projecttypes_get(db: Session = Depends(get_db)) -> dict:
    return projecttypes(db=db)


@router.get("/jobtypes", dependencies=[Depends(lenient_rate_limit)])
def jobtypes(db: Session = Depends(get_db)) -> dict:
    """GET /jobtypes — status, message, jobTypes (Laravel uses camelCase)."""
    rows = (
        db.query(JobType)
        .filter(JobType.active == 1, JobType.hide_from_customers == 0)
        .order_by(JobType.name.asc())
        .all()
    )
    return _success_with_collection(
        "Job Types Loaded Successfully",
        "jobTypes",
        [lookup_to_laravel_resource(r) for r in rows],
    )


@router.get("/jobtypes/get", dependencies=[Depends(lenient_rate_limit)])
def jobtypes_get(db: Session = Depends(get_db)) -> dict:
    return jobtypes(db=db)


@router.get("/reasons", dependencies=[Depends(lenient_rate_limit)])
def reasons(
    db: Session = Depends(get_db),
    tag: Optional[str] = Query(None),
) -> dict:
    """GET /reasons — status, message, reasons. Laravel requires tag; without it return empty."""
    if not tag:
        return _success_with_collection("Reasons Loaded Successfully", "reasons", [])
    q = db.query(Reason).filter(Reason.active == 1)
    if tag:
        q = q.filter(Reason.tags.ilike(f"%{tag}%"))
    rows = q.order_by(Reason.name.asc()).all()
    return _success_with_collection(
        "Reasons Loaded Successfully",
        "reasons",
        [reason_to_laravel_resource(r) for r in rows],
    )


@router.get("/reasons/get", dependencies=[Depends(lenient_rate_limit)])
def reasons_get(
    db: Session = Depends(get_db),
    tag: Optional[str] = Query(None),
) -> dict:
    return reasons(db=db, tag=tag)


@router.get("/referrals", dependencies=[Depends(lenient_rate_limit)])
def referrals(db: Session = Depends(get_db)) -> dict:
    """GET /referrals — status, message, referrals."""
    rows = (
        db.query(Referral)
        .filter(Referral.active == 1)
        .order_by(Referral.name.asc())
        .all()
    )
    return _success_with_collection(
        "Referrals Loaded Successfully",
        "referrals",
        [referral_to_laravel_resource(r) for r in rows],
    )


@router.get("/referrals/get", dependencies=[Depends(lenient_rate_limit)])
def referrals_get(db: Session = Depends(get_db)) -> dict:
    return referrals(db=db)


@router.get("/location", dependencies=[Depends(lenient_rate_limit)])
def location(
    db: Session = Depends(get_db),
    search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
) -> dict:
    """GET /location — status, message, locations, total, page."""
    q = db.query(Location)
    if search:
        q = q.filter(
            (Location.city_ascii.ilike(f"%{search}%"))
            | (Location.country.ilike(f"%{search}%"))
        )
    total = q.count()
    per_page = 15
    rows = q.offset((page - 1) * per_page).limit(per_page).all()
    return {
        "status": "success",
        "message": "Locations Loaded Successfully",
        "locations": [location_to_laravel_resource(r) for r in rows],
        "total": total,
        "page": page,
    }


@router.get("/location/{id}", dependencies=[Depends(lenient_rate_limit)])
def location_by_id(
    id: str,
    db: Session = Depends(get_db),
) -> dict:
    """GET /location/{id} — id is uuid; fetch by uuid."""
    loc = db.query(Location).filter(Location.uuid == id).first()
    if not loc:
        return {"status": "error", "message": "Location not found", "location": {}}
    return {
        "status": "success",
        "message": "Location Loaded Successfully",
        "location": location_to_laravel_resource(loc),
    }
