from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.auth.auth_controller import AuthController
from app.api.auth.schemas import (
    AuthInitRequest,
    AuthInitResponse,
    AuthLoginRequest,
    AuthLoginResponse,
    AuthNewPasswordRequest,
    AuthOtpRequest,
    AuthPasswordChangeRequest,
    AuthRegisterRequest,
    AuthResetRequest,
    AuthVerifyOtpRequest,
    AuthVerifyRequest,
    StatusMessageResponse,
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


@router.post("/init", response_model=AuthInitResponse)
def auth_init(
    payload: AuthInitRequest,
    controller: AuthController = Depends(get_controller),
) -> AuthInitResponse:
    """
    POST /auth/init

    Middlewares in Laravel: none.
    """
    return controller.init(payload)


@router.post("/login", response_model=AuthLoginResponse)
def auth_login(
    payload: AuthLoginRequest,
    controller: AuthController = Depends(get_controller),
) -> AuthLoginResponse:
    """
    POST /auth/login

    Middlewares in Laravel: none.
    """
    return controller.login(payload)


@router.post(
    "/social",
    dependencies=[Depends(strict_rate_limit)],
    response_model=AuthLoginResponse,
)
def auth_social(
    controller: AuthController = Depends(get_controller),
) -> AuthLoginResponse:
    """
    POST /auth/social

    Middlewares in Laravel: api.strict
    """
    # Detailed social flow delegated to AuthService; stub for now.
    raise NotImplementedError("Social auth not yet implemented.")


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


@router.post(
    "/reset",
    dependencies=[Depends(strict_rate_limit)],
    response_model=StatusMessageResponse,
)
def auth_reset(
    payload: AuthResetRequest,
    controller: AuthController = Depends(get_controller),
) -> StatusMessageResponse:
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


@router.post(
    "/otp/reset",
    dependencies=[Depends(otp_rate_limit)],
    response_model=StatusMessageResponse,
)
def auth_otp_reset(
    payload: AuthOtpRequest,
    controller: AuthController = Depends(get_controller),
) -> StatusMessageResponse:
    """
    POST /auth/otp/reset

    Middlewares in Laravel: api.otp
    """
    return controller.resetotp(payload)


@router.post(
    "/otp/verify",
    dependencies=[Depends(otp_rate_limit)],
    response_model=StatusMessageResponse,
)
def auth_otp_verify(
    payload: AuthVerifyOtpRequest,
    controller: AuthController = Depends(get_controller),
) -> StatusMessageResponse:
    """
    POST /auth/otp/verify

    Middlewares in Laravel: api.otp
    """
    return controller.verifyotp(payload)


@router.post(
    "/otp",
    dependencies=[Depends(otp_rate_limit), Depends(require_auth)],
    response_model=StatusMessageResponse,
)
def auth_otp(
    payload: AuthOtpRequest,
    controller: AuthController = Depends(get_controller),
) -> StatusMessageResponse:
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


@router.post(
    "/logout",
    dependencies=[Depends(strict_rate_limit), Depends(require_auth)],
    response_model=StatusMessageResponse,
)
def auth_logout(
    controller: AuthController = Depends(get_controller),
) -> StatusMessageResponse:
    """
    POST /auth/logout

    Middlewares in Laravel: api.strict, auth:sanctum
    """
    return controller.logout()


@router.post(
    "/password",
    dependencies=[Depends(strict_rate_limit), Depends(require_auth)],
    response_model=StatusMessageResponse,
)
def auth_password(
    payload: AuthPasswordChangeRequest,
    controller: AuthController = Depends(get_controller),
) -> StatusMessageResponse:
    """
    POST /auth/password

    Middlewares in Laravel: api.strict, auth:sanctum
    """
    return controller.password(payload)

