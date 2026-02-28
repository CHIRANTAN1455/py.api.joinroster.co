from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user_id, require_auth
from app.core.laravel_response import success_with_message
from app.db.session import get_db
from app.services.favourite_service import FavouriteService


router = APIRouter(prefix="/favourite", tags=["favourite"])


def get_favourite_service(db: Session = Depends(get_db)) -> FavouriteService:
    return FavouriteService(db=db)


@router.get("", dependencies=[Depends(require_auth)])
def list_favourites(
    service: FavouriteService = Depends(get_favourite_service),
    current_user_id: int = Depends(get_current_user_id),
):
    favourites = service.list(current_user_id)
    return success_with_message("Favourites Loaded Successfully", favourites=favourites)


@router.post("", dependencies=[Depends(require_auth)])
def create_favourite(
    body: dict = None,
    service: FavouriteService = Depends(get_favourite_service),
    current_user_id: int = Depends(get_current_user_id),
):
    editor_uuid = body.get("editor_uuid", "") if body else ""
    favourite = service.create(current_user_id, editor_uuid)
    return success_with_message("Favourite Created Successfully", favourite=favourite or {})
