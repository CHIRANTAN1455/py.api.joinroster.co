from typing import Optional
from pydantic import BaseModel


class UserUpdateBody(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    username: Optional[str] = None


class UserTimezoneBody(BaseModel):
    timezone: Optional[str] = None
    utc_offset: Optional[str] = None


class UserJobTypesBody(BaseModel):
    job_types: Optional[list] = None


class UserContentVerticalBody(BaseModel):
    content_verticals: Optional[list] = None


class UserPlatformsBody(BaseModel):
    platforms: Optional[list] = None
