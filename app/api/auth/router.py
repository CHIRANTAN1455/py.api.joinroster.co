from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.auth.auth_controller import AuthController
from app.api.auth.schemas import (
    AuthInitRequest,
    AuthLoginRequest,
    AuthNewPasswordRequest,
    AuthOtpRequest,
    AuthPasswordChangeRequest,
    AuthRegisterRequest,
    AuthResetRequest,
    AuthVerifyOtpRequest,
    AuthVerifyRequest,
)
from app.core.dependencies import (
    otp_rate_limit,
    require_auth,
    strict_rate_limit,
)
from app.db.session import get_db


router = APIRouter(prefix="/auth", tags=["auth"])


def get_controller(db: Session = Depends(get_db)) -> AuthController:
    return AuthController(db=db)


@router.post("/init")
def auth_init(
    payload: AuthInitRequest,
    controller: AuthController = Depends(get_controller),
):
    """POST /auth/init — Laravel-exact: status, action, message."""
    return controller.init(payload)


@router.post("/login")
def auth_login(
    payload: AuthLoginRequest,
    controller: AuthController = Depends(get_controller),
):
    """POST /auth/login — Laravel-exact: status, message, user, access_token, token_type."""
    return controller.login(payload)


@router.post("/social", dependencies=[Depends(strict_rate_limit)])
def auth_social(
    controller: AuthController = Depends(get_controller),
):
    """POST /auth/social — Laravel-exact: status, message, user, access_token, token_type."""
    return controller.social(None)


@router.post(
    "/register",
    dependencies=[Depends(strict_rate_limit)],
)
def auth_register(
    payload: AuthRegisterRequest,
    controller: AuthController = Depends(get_controller),
):
    """
    POST /auth/register

    Middlewares in Laravel: api.strict
    """
    return controller.register(payload)


@router.post("/reset", dependencies=[Depends(strict_rate_limit)])
def auth_reset(
    payload: AuthResetRequest,
    controller: AuthController = Depends(get_controller),
):
    """
    POST /auth/reset

    Middlewares in Laravel: api.strict
    """
    return controller.reset(payload)


@router.post(
    "/new-password",
    dependencies=[Depends(strict_rate_limit)],
)
def auth_new_password(
    payload: AuthNewPasswordRequest,
    controller: AuthController = Depends(get_controller),
):
    """
    POST /auth/new-password

    Middlewares in Laravel: api.strict
    """
    return controller.new_password(payload)


@router.post("/otp/reset", dependencies=[Depends(otp_rate_limit)])
def auth_otp_reset(
    payload: AuthOtpRequest,
    controller: AuthController = Depends(get_controller),
):
    """
    POST /auth/otp/reset

    Middlewares in Laravel: api.otp
    """
    return controller.resetotp(payload)


@router.post("/otp/verify", dependencies=[Depends(otp_rate_limit)])
def auth_otp_verify(
    payload: AuthVerifyOtpRequest,
    controller: AuthController = Depends(get_controller),
):
    """
    POST /auth/otp/verify

    Middlewares in Laravel: api.otp
    """
    return controller.verifyotp(payload)


@router.post("/otp", dependencies=[Depends(otp_rate_limit), Depends(require_auth)])
def auth_otp(
    payload: AuthOtpRequest,
    controller: AuthController = Depends(get_controller),
):
    """
    POST /auth/otp

    Middlewares in Laravel: api.otp, auth:sanctum
    """
    return controller.otp(payload)


@router.post(
    "/verify",
    dependencies=[Depends(otp_rate_limit), Depends(require_auth)],
)
def auth_verify(
    payload: AuthVerifyRequest,
    controller: AuthController = Depends(get_controller),
):
    """
    POST /auth/verify

    Middlewares in Laravel: api.otp, auth:sanctum
    """
    return controller.verify(payload)


@router.post("/logout", dependencies=[Depends(strict_rate_limit), Depends(require_auth)])
def auth_logout(
    controller: AuthController = Depends(get_controller),
):
    """
    POST /auth/logout

    Middlewares in Laravel: api.strict, auth:sanctum
    """
    return controller.logout()


@router.post("/password", dependencies=[Depends(strict_rate_limit), Depends(require_auth)])
def auth_password(
    payload: AuthPasswordChangeRequest,
    controller: AuthController = Depends(get_controller),
):
    """
    POST /auth/password

    Middlewares in Laravel: api.strict, auth:sanctum
    """
    return controller.password(payload)

