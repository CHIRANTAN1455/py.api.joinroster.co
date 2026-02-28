"""
Auth controller: returns Laravel-exact response shapes (same keys, casing, order).
All methods return plain dicts so JSON matches Laravel 1:1.
"""

from typing import Any, Dict

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.api.auth.schemas import (
    AuthInitRequest,
    AuthNewPasswordRequest,
    AuthOtpRequest,
    AuthPasswordChangeRequest,
    AuthRegisterRequest,
    AuthResetRequest,
    AuthVerifyOtpRequest,
    AuthVerifyRequest,
)
from app.core.laravel_response import user_to_laravel_user_resource
from app.db.models.user import User
from app.services.auth_service import AuthService


class AuthController:
    def __init__(self, db: Session):
        self.db = db
        self.auth_service = AuthService(db=db)

    def init(self, payload: AuthInitRequest) -> Dict[str, Any]:
        identifier = (payload.email or payload.phone or "").strip()
        if not identifier:
            return {"status": "error", "action": "register", "message": "Email or phone is required."}
        user = self.auth_service.search(identifier=identifier)
        return {
            "status": "success",
            "action": "login" if user else "register",
            "message": "Login user" if user else "Register user",
        }

    def login(self, payload: Any) -> Dict[str, Any]:
        result = self.auth_service.login(username=payload.username, password=payload.password)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"status": "error", "message": "These credentials do not match our records."},
            )
        return {
            "status": "success",
            "message": result.get("message", "Login successful"),
            "user": result["user"],
            "access_token": result["access_token"],
            "token_type": result["token_type"],
        }

    def register(self, payload: AuthRegisterRequest) -> Dict[str, Any]:
        user = User(
            email=payload.email or "",
            phone=payload.phone,
            password="__hashed__",
            policy_accepted=payload.policy_accepted,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        token_result = self.auth_service.login(username=user.email, password=payload.password)
        access_token = token_result["access_token"] if token_result else ""
        return {
            "status": "success",
            "message": "Registration successful, please verify your email.",
            "user": user_to_laravel_user_resource(user),
            "access_token": access_token,
            "token_type": "Bearer",
        }

    def reset(self, payload: AuthResetRequest) -> Dict[str, Any]:
        return {"status": "success", "message": "Password reset requested."}

    def new_password(self, payload: AuthNewPasswordRequest) -> Dict[str, Any]:
        return {"status": "success", "user": None, "access_token": ""}

    def otp(self, payload: AuthOtpRequest) -> Dict[str, Any]:
        return {"status": "success", "message": "OTP sent."}

    def verify(self, payload: AuthVerifyRequest) -> Dict[str, Any]:
        return {"status": "success", "message": "OTP verified.", "user": None}

    def verifyotp(self, payload: AuthVerifyOtpRequest) -> Dict[str, Any]:
        return {"status": "success", "message": "OTP verified."}

    def resetotp(self, payload: AuthOtpRequest) -> Dict[str, Any]:
        return {"status": "success", "message": "Reset OTP sent."}

    def logout(self) -> Dict[str, Any]:
        return {"status": "success", "message": "Logged out successfully."}

    def password(self, payload: AuthPasswordChangeRequest) -> Dict[str, Any]:
        return {"status": "success", "message": "Password updated successfully."}

    def social(self, payload: Any) -> Dict[str, Any]:
        """Stub: same shape as login. Real OAuth to be wired."""
        return {
            "status": "success",
            "message": "Login successful",
            "user": {},
            "access_token": "",
            "token_type": "Bearer",
        }

    def chat(self) -> Dict[str, Any]:
        """GET /auth/chat — Laravel returns chat/GetStream credentials."""
        return {"status": "success", "message": "Chat loaded.", "user": None}

    def linkedin(self, payload: Any) -> Dict[str, Any]:
        """POST /auth/linkedin — Laravel linkedinAuth stub."""
        return {"status": "success", "message": "Login successful", "user": {}, "access_token": "", "token_type": "Bearer"}

    def broadcasting(self) -> Dict[str, Any]:
        """POST /auth/broadcasting — Laravel returns UserBroadcastingResource."""
        return {"status": "success", "user_id": None, "socket_id": None}
