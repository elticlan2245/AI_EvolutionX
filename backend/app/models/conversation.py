from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from bson import ObjectId

class Message(BaseModel):
    role: str
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    tokens: Optional[int] = None
    model: Optional[str] = None

class Conversation(BaseModel):
    id: Optional[str] = Field(alias="_id")
    title: str
    messages: List[Message] = []
    model: str = "llama3.1:8b"
    user_id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    tags: List[str] = []
    starred: bool = False
    
    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}
