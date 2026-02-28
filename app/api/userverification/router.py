"""UserVerification. Path {id} = uuid. Laravel-exact: status, message, verification/verifications."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user_id, require_auth
from app.core.laravel_response import success_with_message
from app.db.session import get_db
from app.services.user_verification_service import UserVerificationService


router = APIRouter(prefix="/userverification", tags=["userverification"])


def get_service(db: Session = Depends(get_db)) -> UserVerificationService:
    return UserVerificationService(db=db)


@router.get("", dependencies=[Depends(require_auth)])
def list_userverification(
    service: UserVerificationService = Depends(get_service),
    current_user_id: int = Depends(get_current_user_id),
):
    verifications = service.list(current_user_id)
    return success_with_message("Verification Links Loaded Successfully", verifications=verifications)


@router.post("", dependencies=[Depends(require_auth)])
def create_userverification(
    service: UserVerificationService = Depends(get_service),
    current_user_id: int = Depends(get_current_user_id),
):
    verification = service.create(current_user_id, None)
    return success_with_message("Verification Created Successfully", verification=verification or {})


@router.post("/many", dependencies=[Depends(require_auth)])
def create_many_userverification(
    service: UserVerificationService = Depends(get_service),
    current_user_id: int = Depends(get_current_user_id),
):
    v1 = service.create(current_user_id, None)
    verifications = [v1] if v1 else []
    return success_with_message("Verifications Created Successfully", verifications=verifications)


@router.delete("/{id}", dependencies=[Depends(require_auth)])
def delete_userverification(
    id: str,
    service: UserVerificationService = Depends(get_service),
    current_user_id: int = Depends(get_current_user_id),
):
    ok = service.delete(id, current_user_id)
    if not ok:
        return {"status": "error", "message": "Verification not found"}
    return success_with_message("Verification Deleted Successfully")
