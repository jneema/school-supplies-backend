from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, ARRAY, JSON, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    products = relationship("Product", back_populates="category")

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)
    old_price = Column(Float, nullable=True)
    category_id = Column(Integer, ForeignKey("categories.id"))
    color = Column(String, nullable=True)
    colors = Column(ARRAY(String), nullable=True)
    rating = Column(Float, nullable=True)
    review_count = Column(Integer, nullable=True)
    description = Column(String, nullable=True)
    features = Column(ARRAY(String), nullable=True)
    specifications = Column(JSON, nullable=True)
    tags = Column(String, nullable=True)
    in_stock = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    category = relationship("Category", back_populates="products")