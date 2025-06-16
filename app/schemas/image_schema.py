from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ImageResponse(BaseModel):
    id: int
    image_url: str
    public_id: str
    created_at: datetime
    class Config:
        orm_mode = True