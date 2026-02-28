from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.session import get_db


router = APIRouter(prefix="/health", tags=["health"])


@router.get("/db")
def db_health(db: Session = Depends(get_db)):
    """
    Simple database connectivity check.

    Returns a 200 response with status information and, if possible, the total
    number of users from the `users` table. This is an internal diagnostic
    endpoint and does not exist in the original Laravel API.
    """
    try:
        db.execute(text("SELECT 1"))
        result = db.execute(text("SELECT COUNT(*) FROM users"))
        users_count = result.scalar()
        return {
            "status": "success",
            "database": {"ok": True, "users_count": int(users_count or 0)},
        }
    except Exception as exc:  # pragma: no cover - diagnostic path
        return {
            "status": "error",
            "database": {"ok": False, "error": str(exc)},
        }

