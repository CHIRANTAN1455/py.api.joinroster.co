from fastapi import APIRouter, Depends

from app.core.dependencies import require_auth


router = APIRouter(prefix="/profile", tags=["profile"])


@router.get("", dependencies=[Depends(require_auth)])
def get_profile():
    """
    GET /profile
    Middleware: auth:sanctum
    """
    return {"status": "success"}


@router.get("/statistics", dependencies=[Depends(require_auth)])
def get_profile_statistics():
    """
    GET /profile/statistics
    Middleware: auth:sanctum
    """
    return {"status": "success"}


@router.get("/social", dependencies=[Depends(require_auth)])
def get_profile_social():
    """
    GET /profile/social
    Middleware: auth:sanctum
    """
    return {"status": "success"}


@router.post("/update", dependencies=[Depends(require_auth)])
def update_profile():
    """
    POST /profile/update
    Middleware: auth:sanctum
    """
    return {"status": "success"}


@router.post("/pricing", dependencies=[Depends(require_auth)])
def update_profile_pricing():
    """
    POST /profile/pricing
    Middleware: auth:sanctum
    """
    return {"status": "success"}


@router.post("/pricing/no-delete", dependencies=[Depends(require_auth)])
def update_profile_pricing_no_delete():
    """
    POST /profile/pricing/no-delete
    Middleware: auth:sanctum
    """
    return {"status": "success"}


@router.post("/skills", dependencies=[Depends(require_auth)])
def update_profile_skills():
    """
    POST /profile/skills
    Middleware: auth:sanctum
    """
    return {"status": "success"}


@router.post("/jobtypes", dependencies=[Depends(require_auth)])
def update_profile_jobtypes():
    """
    POST /profile/jobtypes
    Middleware: auth:sanctum
    """
    return {"status": "success"}


@router.post("/contentverticals", dependencies=[Depends(require_auth)])
def update_profile_contentverticals():
    """
    POST /profile/contentverticals
    Middleware: auth:sanctum
    """
    return {"status": "success"}


@router.post("/contentverticals/new", dependencies=[Depends(require_auth)])
def add_profile_contentverticals():
    """
    POST /profile/contentverticals/new
    Middleware: auth:sanctum
    """
    return {"status": "success"}


@router.post("/platforms", dependencies=[Depends(require_auth)])
def update_profile_platforms():
    """
    POST /profile/platforms
    Middleware: auth:sanctum
    """
    return {"status": "success"}


@router.post("/softwares", dependencies=[Depends(require_auth)])
def update_profile_softwares():
    """
    POST /profile/softwares
    Middleware: auth:sanctum
    """
    return {"status": "success"}


@router.post("/equipments", dependencies=[Depends(require_auth)])
def update_profile_equipments():
    """
    POST /profile/equipments
    Middleware: auth:sanctum
    """
    return {"status": "success"}


@router.post("/creativestyles", dependencies=[Depends(require_auth)])
def update_profile_creativestyles():
    """
    POST /profile/creativestyles
    Middleware: auth:sanctum
    """
    return {"status": "success"}

