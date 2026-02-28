from typing import Optional
from pydantic import BaseModel


class ProjectApplicationAddBody(BaseModel):
    project_uuid: Optional[str] = None


class ProjectApplicationUpdateBody(BaseModel):
    status: Optional[str] = None


class ProjectApplicationNoteBody(BaseModel):
    note: Optional[str] = None


class ProjectApplicationRejectionBody(BaseModel):
    application_uuid: Optional[str] = None
