from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.session import get_db


router = APIRouter(prefix="/health", tags=["health"])


@router.get("/db")
def db_health(db: Session = Depends(get_db)):
    """
    Simple database connectivity check.
    Uses a minimal SELECT 1 to avoid timeouts on large tables.
    """
    try:
        db.execute(text("SELECT 1"))
        return {"status": "success", "database": {"ok": True}}
    except Exception as exc:  # pragma: no cover - diagnostic path
        return {
            "status": "error",
            "database": {"ok": False, "error": str(exc)},
        }

