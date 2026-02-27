from typing import Any, Dict, List, Optional

from pydantic import BaseModel


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

