# app/models/image.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.database import Base
from datetime import datetime

class Image(Base):
    
    __tablename__ = "images"
    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String, nullable=False)
    public_id = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True) 
    product_id = Column(Integer, ForeignKey("products.id"), nullable=True)  
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)  
    created_at = Column(DateTime, default=datetime.utcnow)