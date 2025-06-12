# Project model for the projects feature

from pydantic import BaseModel, Field
from typing import Optional, Annotated
from bson import ObjectId
from datetime import datetime

class ProjectBase(BaseModel):
    name: str = Field(..., max_length=100)
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Project(ProjectBase):
    id: Optional[str] = Field(default=None, alias="_id")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    model_config = {
        "validate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str}
    }
