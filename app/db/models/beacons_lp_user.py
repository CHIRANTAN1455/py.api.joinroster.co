from sqlalchemy import Column, Integer, String

from app.db.base import Base


class BeaconsLpUser(Base):
    """
    Minimal SQLAlchemy representation of Laravel's `BeaconsLpUser` model.

    Table: beacons_lp_user
    Columns used by pdfsend:
      - id (auto-increment)
      - email
      - name
      - fol_count
    """

    __tablename__ = "beacons_lp_user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), nullable=False)
    name = Column(String(255), nullable=True)
    fol_count = Column(String(255), nullable=True)

