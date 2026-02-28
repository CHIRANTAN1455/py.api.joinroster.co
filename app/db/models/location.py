from sqlalchemy import Column, Float, Integer, String

from app.db.base import Base


class Location(Base):
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
    population = Column(Integer, nullable=True)
    lat = Column(Float, nullable=True)
    lng = Column(Float, nullable=True)
    timezone = Column(String(100), nullable=True)
    utc_offset = Column(String(20), nullable=True)
