from typing import Any, Dict, Optional

from sqlalchemy.orm import Session

from app.core.laravel_response import user_to_laravel_user_resource
from app.core.security import create_access_token
from app.db.models.user import User


class AuthService:
    """
    Python equivalent of Laravel's AuthService.

    Responsibilities (from migration spec):
    - search user by identifier (email/phone)
    - login with username/password
    - social OAuth auth/register
    - register user
    - OTP generation/verification
    - password reset
    - chat token generation
    """

    def __init__(self, db: Session):
        self.db = db

    def search(self, identifier: str) -> Optional[User]:
        return (
            self.db.query(User)
            .filter((User.email == identifier) | (User.phone == identifier))
            .first()
        )

    def login(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        # NOTE: password verification and hashing must be wired to match Laravel.
        user = (
            self.db.query(User)
            .filter((User.email == username) | (User.username == username))
            .first()
        )
        if not user:
            return None

        # TODO: verify hashed password against Laravel hash algorithm.

        token = create_access_token(subject=str(user.id))
        return {
            "message": "Login successful",
            "user": user_to_laravel_user_resource(user),
            "access_token": token,
            "token_type": "Bearer",
        }

