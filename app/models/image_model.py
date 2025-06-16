from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base
from datetime import datetime

class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String, nullable=False)
    public_id = Column(String, nullable=False)  
    created_at = Column(DateTime, default=datetime.utcnow)