from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class UserPlan(str, Enum):
    free = "free"
    premium = "premium"
    pro = "pro"

class User(BaseModel):
    id: Optional[str] = Field(alias="_id", default=None)
    email: EmailStr
    username: str
    hashed_password: str
    plan: UserPlan = UserPlan.free
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None
    is_active: bool = True
    is_verified: bool = False
    monthly_messages: int = 0
    monthly_limit: int = 100
    voice_enabled: bool = False
    
    class Config:
        populate_by_name = True

class UserRegister(BaseModel):
    email: EmailStr
    username: str
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user: dict
