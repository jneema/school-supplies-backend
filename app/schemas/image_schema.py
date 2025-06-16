from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ImageResponse(BaseModel):
    id: int
    image_url: str
    public_id: str
    user_id: Optional[int] = None
    product_id: Optional[int] = None
    category_id: Optional[int] = None
    created_at: datetime
    class Config:
        orm_mode = True