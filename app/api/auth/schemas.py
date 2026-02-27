from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class AuthInitRequest(BaseModel):
    email: Optional[str] = Field(None, max_length=255)
    phone: Optional[str] = Field(None, max_length=255)


class AuthInitResponse(BaseModel):
    status: str
    action: str
    message: str

    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "action": "login",
                "message": "User found, proceed to login.",
            }
        }


class AuthLoginRequest(BaseModel):
    username: str = Field(..., max_length=255)
    password: str = Field(..., max_length=255)


class AuthLoginResponse(BaseModel):
    status: str
    user: Dict[str, Any]
    access_token: str
    token_type: str

    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "user": {"id": 1, "email": "user@example.com"},
                "access_token": "jwt-token-here",
                "token_type": "Bearer",
            }
        }


class AuthSocialRequest(BaseModel):
    access_token: str
    provider: str
    referral_code_used: Optional[str] = None


class AuthRegisterRequest(BaseModel):
    email: Optional[str] = Field(None, max_length=255)
    phone: Optional[str] = Field(None, max_length=255)
    password: str = Field(..., max_length=255)
    referral_code_used: Optional[str] = None
    policy_accepted: bool


class AuthResetRequest(BaseModel):
    email: str = Field(..., max_length=255)
    password: str = Field(..., max_length=255)
    otp: str = Field(..., max_length=255)


class AuthNewPasswordRequest(BaseModel):
    token: str
    password: str


class AuthOtpRequest(BaseModel):
    email: str = Field(..., max_length=255)


class AuthVerifyOtpRequest(BaseModel):
    email: str = Field(..., max_length=255)
    otp: str


class AuthVerifyRequest(BaseModel):
    otp: str


class AuthPasswordChangeRequest(BaseModel):
    current_password: str
    new_password: str
    confirm_password: str


class StatusMessageResponse(BaseModel):
    status: str
    message: str

    class Config:
        json_schema_extra = {
            "example": {"status": "success", "message": "OK"},
        }

