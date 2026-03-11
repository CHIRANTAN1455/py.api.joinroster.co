from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class User(Base):
    """
    SQLAlchemy representation of Laravel's `User` model.

    Table name, fillable attributes, and relationships are derived from the
    fastapi_migration_spec.json. Not all columns are explicitly modeled yet,
    but the table name and primary key align with Laravel.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(36), unique=True, index=True, nullable=True)
    photo = Column(String(500), nullable=True)
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    name = Column(String(255), nullable=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    phone = Column(String(255), nullable=True)
    username = Column(String(255), unique=True, index=True, nullable=True)
    address = Column(String(255), nullable=True)
    city = Column(String(255), nullable=True)
    country = Column(String(255), nullable=True)
    company = Column(String(255), nullable=True)
    job_title = Column(String(255), nullable=True)
    fun_fact = Column(String(3000), nullable=True)
    reference = Column(String(255), nullable=True)
    timezone = Column(String(255), nullable=True)
    utc_offset = Column(String(20), nullable=True)
    account_type = Column(String(255), nullable=True)
    open_for_work = Column(Integer, default=0, nullable=True)
    latitude = Column(String(50), nullable=True)
    longitude = Column(String(50), nullable=True)
    password = Column(String(255), nullable=False)
    email_verified_at = Column(DateTime, nullable=True)
    phone_verified_at = Column(DateTime, nullable=True)
    verified_at = Column(DateTime, nullable=True)
    policy_accepted = Column(Boolean, default=False)
    policy_accepted_at = Column(DateTime, nullable=True)
    active = Column(Boolean, default=True)

    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)

    # Relationships (defined with string targets so models can be added later)
    # Explicitly specify foreign_keys to disambiguate user_id vs editor_id on Project.
    projects = relationship(
        "Project",
        back_populates="user",
        lazy="selectin",
        foreign_keys="Project.user_id",
    )

