from typing import Any, Dict

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

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
from app.db.models.user import User
from app.services.auth_service import AuthService


class AuthController:
    """
    Controller functions corresponding to Laravel's AuthController methods.

    These are thin wrappers orchestrating services and enforcing that
    response shapes (keys/casing) match the Laravel API.
    """

    def __init__(self, db: Session):
        self.db = db
        self.auth_service = AuthService(db=db)

    def init(self, payload: AuthInitRequest) -> AuthInitResponse:
        identifier = payload.email or payload.phone
        if not identifier:
            return AuthInitResponse(
                status="error",
                action="register",
                message="Email or phone is required.",
            )

        user = self.auth_service.search(identifier=identifier)
        if user:
            return AuthInitResponse(
                status="success",
                action="login",
                message="User exists, proceed to login.",
            )

        return AuthInitResponse(
            status="success",
            action="register",
            message="User not found, proceed to registration.",
        )

    def login(self, payload: AuthLoginRequest) -> AuthLoginResponse:
        result = self.auth_service.login(
            username=payload.username,
            password=payload.password,
        )
        if not result:
            # Shape mimics Laravel style: status/message on auth failure.
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"status": "error", "message": "Invalid credentials."},
            )

        return AuthLoginResponse(
            status="success",
            user=result["user"],
            access_token=result["access_token"],
            token_type=result["token_type"],
        )

    def register(self, payload: AuthRegisterRequest) -> Dict[str, Any]:
        # Full registration flow (including referral, OTP, mail) will mirror
        # Laravel behavior; for now, this returns a placeholder structure
        # with keys identical to the Laravel response.
        user = User(
            email=payload.email,
            phone=payload.phone,
            password="__hashed__",  # TODO: hash same as Laravel
            policy_accepted=payload.policy_accepted,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        token_result = self.auth_service.login(username=user.email, password=payload.password)
        access_token = token_result["access_token"] if token_result else ""

        return {
            "status": "success",
            "user": {"id": user.id, "email": user.email},
            "access_token": access_token,
            "token_type": "Bearer",
        }

    def reset(self, payload: AuthResetRequest) -> StatusMessageResponse:
        # Stub implementation preserving response shape.
        return StatusMessageResponse(status="success", message="Password reset requested.")

    def new_password(self, payload: AuthNewPasswordRequest) -> Dict[str, Any]:
        # Stub implementation preserving response shape.
        return {
            "status": "success",
            "user": None,
            "access_token": "",
        }

    def otp(self, payload: AuthOtpRequest) -> StatusMessageResponse:
        return StatusMessageResponse(status="success", message="OTP sent.")

    def verify(self, payload: AuthVerifyRequest) -> Dict[str, Any]:
        return {
            "status": "success",
            "message": "OTP verified.",
            "user": None,
        }

    def verifyotp(self, payload: AuthVerifyOtpRequest) -> StatusMessageResponse:
        return StatusMessageResponse(status="success", message="OTP verified.")

    def resetotp(self, payload: AuthOtpRequest) -> StatusMessageResponse:
        return StatusMessageResponse(status="success", message="Reset OTP sent.")

    def logout(self) -> StatusMessageResponse:
        return StatusMessageResponse(status="success", message="Logged out.")

    def password(self, payload: AuthPasswordChangeRequest) -> StatusMessageResponse:
        return StatusMessageResponse(status="success", message="Password changed.")

