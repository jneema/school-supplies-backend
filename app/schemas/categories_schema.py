from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Dict

class Specification(BaseModel):
    name: str
    value: str

class CategoryCreate(BaseModel):
    category_name: str
    image_link: Optional[str] = None
    created_at: Optional[datetime] = None

class CategoryResponse(BaseModel):
    id: int
    category_name: str
    image_link: Optional[str] = None
    created_at: datetime
    class Config:
        orm_mode = True

class ProductCreate(BaseModel):
    name: str
    price: float  
    old_price: Optional[float] = None 
    category_id: Optional[int] = None
    category: Optional[str] = None
    color: Optional[str] = None
    colors: Optional[List[str]] = None
    rating: Optional[float] = None
    review_count: Optional[int] = None
    description: Optional[str] = None
    image_link: Optional[str] = None
    features: Optional[List[str]] = None
    specifications: Optional[List[Specification]] = None
    tags: Optional[str] = None
    in_stock: Optional[bool] = True
    created_at: Optional[datetime] = None

class ProductUpdate(BaseModel):  
    name: Optional[str] = None
    price: Optional[float] = None
    old_price: Optional[float] = None
    category_id: Optional[int] = None
    category: Optional[str] = None
    color: Optional[str] = None
    colors: Optional[List[str]] = None
    rating: Optional[float] = None
    review_count: Optional[int] = None
    description: Optional[str] = None
    image_link: Optional[str] = None
    features: Optional[List[str]] = None
    specifications: Optional[List[Specification]] = None
    tags: Optional[str] = None
    in_stock: Optional[bool] = None

class ProductResponse(BaseModel):
    id: int
    name: str
    price: float
    old_price: Optional[float] = None
    category_id: int
    color: Optional[str] = None
    colors: Optional[List[str]] = None
    rating: Optional[float] = None
    review_count: Optional[int] = None
    image_link: Optional[str] = None
    description: Optional[str] = None
    features: Optional[List[str]] = None
    specifications: Optional[List[Dict]] = None
    tags: Optional[str] = None
    in_stock: bool
    created_at: datetime
    class Config:
        orm_mode = True