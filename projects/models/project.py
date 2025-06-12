# Project model for the projects feature

from pydantic import BaseModel, Field
from typing import Optional, Annotated
from bson import ObjectId

class ProjectBase(BaseModel):
    name: str = Field(..., max_length=100)
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None

class Project(ProjectBase):
    id: Optional[str] = Field(default=None, alias="_id")
    
    model_config = {
        "validate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str}
    }
