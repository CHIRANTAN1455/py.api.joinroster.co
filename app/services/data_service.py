"""Data: editors, countries, states, cities, locations from DB."""
from typing import Any, Dict, List

from sqlalchemy.orm import Session

from app.core.laravel_response import user_to_laravel_user_resource
from app.db.models.location import Location
from app.db.models.user import User


class DataService:
    def __init__(self, db: Session):
        self.db = db

    def editors(self, payload: Any = None) -> List[Dict]:
        try:
            users = self.db.query(User).filter(User.active.is_(True)).limit(100).all()
            return [user_to_laravel_user_resource(u) for u in users]
        except Exception:
            return []

    def countries(self, payload: Any = None) -> List[str]:
        try:
            rows = self.db.query(Location.country).filter(Location.country.isnot(None)).distinct().limit(200).all()
            return [r[0] for r in rows if r[0]]
        except Exception:
            return []

    def states(self, payload: Any = None) -> List[str]:
        try:
            rows = self.db.query(Location.admin_name).filter(Location.admin_name.isnot(None)).distinct().limit(200).all()
            return [r[0] for r in rows if r[0]]
        except Exception:
            return []

    def cities(self, payload: Any = None) -> List[str]:
        try:
            rows = self.db.query(Location.city).filter(Location.city.isnot(None)).distinct().limit(200).all()
            return [r[0] for r in rows if r[0]]
        except Exception:
            return []

    def locations(self, payload: Any = None) -> List[Dict]:
        try:
            items = self.db.query(Location).limit(100).all()
            return [{"uuid": loc.uuid, "city": loc.city, "city_ascii": loc.city_ascii, "country": loc.country} for loc in items]
        except Exception:
            return []
