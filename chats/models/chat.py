# Chat model for the chat history feature

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from bson import ObjectId

class ChatBase(BaseModel):
    user_query: str = Field(..., max_length=2000)
    ai_response: str = Field(..., max_length=10000)
    model_used: str = Field(default="llama3.3")
    support_level: Optional[str] = None
    routing_reason: Optional[str] = None

class ChatCreate(ChatBase):
    pass

class Chat(ChatBase):
    id: Optional[str] = Field(default=None, alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    model_config = {
        "validate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str}
    }
