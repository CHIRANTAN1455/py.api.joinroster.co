from typing import Optional, Union
from pydantic import BaseModel, field_validator


class UserUpdateBody(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    username: Optional[str] = None


class UserTimezoneBody(BaseModel):
    timezone: Optional[str] = None
    utc_offset: Optional[Union[str, int, float]] = None

    @field_validator("utc_offset", mode="before")
    @classmethod
    def utc_offset_to_str(cls, v):
        if v is None:
            return None
        return str(v)


class UserJobTypesBody(BaseModel):
    job_types: Optional[list] = None


class UserContentVerticalBody(BaseModel):
    content_verticals: Optional[list] = None


class UserPlatformsBody(BaseModel):
    platforms: Optional[list] = None
