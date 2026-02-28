"""
Pydantic schemas for the profile domain.

These can be expanded to mirror Laravel's resource transformers exactly.
"""
from typing import Optional

from pydantic import BaseModel


class ProfileUpdateBody(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    username: Optional[str] = None

