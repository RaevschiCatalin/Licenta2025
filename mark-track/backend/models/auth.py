from pydantic import BaseModel, EmailStr, constr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: constr(min_length=8)
    role: str = "pending"

class UserLogin(UserBase):
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None

class UserResponse(UserBase):
    id: str
    role: str
    created_at: datetime

    class Config:
        from_attributes = True 