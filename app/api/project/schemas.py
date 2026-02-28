from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class ProjectCreateBody(BaseModel):
    title: Optional[str] = ""
    description: Optional[str] = ""
    budget: Optional[Any] = None
    budget_per: Optional[str] = "project"
    status: Optional[str] = "pending"
    published: Optional[int] = 0
    editors: Optional[List[Any]] = None  # list of uuid strings or objects with uuid


class ProjectUpdateBody(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    budget: Optional[Any] = None
    status: Optional[str] = None
    editor_id: Optional[str] = None
    editors: Optional[List[Any]] = None


class ProjectListResponse(BaseModel):
    status: str
    projects: List[Dict[str, Any]]
    total: int
    page: int
    metrics: Dict[str, Any]

    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "projects": [],
                "total": 0,
                "page": 1,
                "metrics": {},
            }
        }


class ProjectResourceResponse(BaseModel):
    status: str
    project: Dict[str, Any]


class PublicProjectWithApplicationResponse(BaseModel):
    status: str
    project: Dict[str, Any]
    application: Optional[Dict[str, Any]] = None


class ProjectStatusResponse(BaseModel):
    status: str
    project: Dict[str, Any]


class ProjectReviewResponse(BaseModel):
    status: str
    review: Dict[str, Any]


class ProjectFeedbackResponse(BaseModel):
    status: str
    feedback: Dict[str, Any]


class ProjectMatchScoreResponse(BaseModel):
    status: str
    match: Dict[str, Any]

