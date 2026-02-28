"""UserVerification. Path {id} = uuid. Laravel-exact: status, message, verification/verifications."""
from fastapi import APIRouter, Depends

from app.core.dependencies import require_auth
from app.core.laravel_response import success_with_message


router = APIRouter(prefix="/userverification", tags=["userverification"])


@router.get("", dependencies=[Depends(require_auth)])
def list_userverification():
    return success_with_message("Verification Links Loaded Successfully", verifications=[])


@router.post("", dependencies=[Depends(require_auth)])
def create_userverification():
    return success_with_message("Verification Created Successfully", verification={})


@router.post("/many", dependencies=[Depends(require_auth)])
def create_many_userverification():
    return success_with_message("Verifications Created Successfully", verifications=[])


@router.delete("/{id}", dependencies=[Depends(require_auth)])
def delete_userverification(id: str):
    return success_with_message("Verification Deleted Successfully")
