"""Data endpoints. Laravel-exact: status, message, editors/countries/states/cities/locations."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import require_auth
from app.core.laravel_response import success_with_message
from app.db.session import get_db
from app.services.data_service import DataService


router = APIRouter(prefix="/data", tags=["data"])


def get_data_service(db: Session = Depends(get_db)) -> DataService:
    return DataService(db=db)


@router.post("/editor", dependencies=[Depends(require_auth)])
def data_editor(
    body: dict = None,
    service: DataService = Depends(get_data_service),
):
    editors = service.editors(body)
    return success_with_message("Editors Loaded Successfully", editors=editors)


@router.post("/country", dependencies=[Depends(require_auth)])
def data_country(
    body: dict = None,
    service: DataService = Depends(get_data_service),
):
    countries = service.countries(body)
    return success_with_message("Countries Loaded Successfully", countries=countries)


@router.post("/state", dependencies=[Depends(require_auth)])
def data_state(
    body: dict = None,
    service: DataService = Depends(get_data_service),
):
    states = service.states(body)
    return success_with_message("States Loaded Successfully", states=states)


@router.post("/city", dependencies=[Depends(require_auth)])
def data_city(
    body: dict = None,
    service: DataService = Depends(get_data_service),
):
    cities = service.cities(body)
    return success_with_message("Cities Loaded Successfully", cities=cities)


@router.post("/location", dependencies=[Depends(require_auth)])
def data_location(
    body: dict = None,
    service: DataService = Depends(get_data_service),
):
    locations = service.locations(body)
    return success_with_message("Locations Loaded Successfully", locations=locations)


@router.post("/editor/invite", dependencies=[Depends(require_auth)])
def data_editor_invite():
    return success_with_message("Invitation sent", editor={})
