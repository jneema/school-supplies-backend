from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    first_name: str 
    last_name: str
    email: EmailStr
    password: str
    phone: str
    is_active: bool = True
    is_admin: bool = False
    created_at: datetime

class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    is_active: bool
    is_admin: bool

    class Config:
        orm_mode = True
