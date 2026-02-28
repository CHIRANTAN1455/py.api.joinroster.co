from fastapi import APIRouter, Depends

from app.core.dependencies import require_auth


router = APIRouter(prefix="/data", tags=["data"])


@router.post("/editor", dependencies=[Depends(require_auth)])
def data_editor():
    return {"status": "success"}


@router.post("/country", dependencies=[Depends(require_auth)])
def data_country():
    return {"status": "success"}


@router.post("/state", dependencies=[Depends(require_auth)])
def data_state():
    return {"status": "success"}


@router.post("/city", dependencies=[Depends(require_auth)])
def data_city():
    return {"status": "success"}


@router.post("/location", dependencies=[Depends(require_auth)])
def data_location():
    return {"status": "success"}


@router.post("/editor/invite", dependencies=[Depends(require_auth)])
def data_editor_invite():
    return {"status": "success"}

