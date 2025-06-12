from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class CategoryCreate(BaseModel):
    category_name: str
    created_at: Optional[datetime] = None 

class CategoryResponse(BaseModel):
    id: int
    category_name: str
    created_at: datetime

    class Config:
        orm_mode = True


class ProductCreate(BaseModel):
    name: str 
    price: float 
    image: str
    category_id: int
    image: Optional[str] = None
    color: Optional[str] = None
    created_at: Optional[datetime] = None
    rating: Optional[float] = None
    reviews: Optional[int] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    created_at: Optional[datetime] = None

class ProductResponse(BaseModel):
    id: int
    name: str 
    price: int
    image: str
    category_id: int
    color: str
    created_at: datetime
    category: CategoryResponse

    class Config:
        orm_mode = True
