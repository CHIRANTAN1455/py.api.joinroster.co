"""Data endpoints. Laravel-exact: status, message, editors/countries/states/cities/locations."""
from fastapi import APIRouter, Depends

from app.core.dependencies import require_auth
from app.core.laravel_response import success_with_message


router = APIRouter(prefix="/data", tags=["data"])


@router.post("/editor", dependencies=[Depends(require_auth)])
def data_editor():
    return success_with_message("Editors Loaded Successfully", editors=[])


@router.post("/country", dependencies=[Depends(require_auth)])
def data_country():
    return success_with_message("Countries Loaded Successfully", countries=[])


@router.post("/state", dependencies=[Depends(require_auth)])
def data_state():
    return success_with_message("States Loaded Successfully", states=[])


@router.post("/city", dependencies=[Depends(require_auth)])
def data_city():
    return success_with_message("Cities Loaded Successfully", cities=[])


@router.post("/location", dependencies=[Depends(require_auth)])
def data_location():
    return success_with_message("Locations Loaded Successfully", locations=[])


@router.post("/editor/invite", dependencies=[Depends(require_auth)])
def data_editor_invite():
    return success_with_message("Invitation sent", editor={})
