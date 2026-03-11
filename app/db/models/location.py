from sqlalchemy import Column, DateTime, Integer, Numeric, String

from app.db.base import Base


class Location(Base):
    """
    Matches Laravel locations table (2023_01_28_002052_create_locations_table).
    Base migration: id, uuid, city, city_ascii, country, iso2, iso3, admin_name,
    capital, population, lat, lng, timestamps, softDeletes.
    No timezone/utc_offset in base migration.
    """
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(36), unique=True, index=True, nullable=True)
    city = Column(String(255), nullable=True)
    city_ascii = Column(String(255), nullable=True)
    country = Column(String(255), nullable=True)
    iso2 = Column(String(10), nullable=True)
    iso3 = Column(String(10), nullable=True)
    admin_name = Column(String(255), nullable=True)
    capital = Column(String(255), nullable=True)
    population = Column(String(20), nullable=True)  # Laravel: string
    lat = Column(Numeric, nullable=True)
    lng = Column(Numeric, nullable=True)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    deleted_at = Column(DateTime, nullable=True)
