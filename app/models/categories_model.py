from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, ARRAY
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base

class Category(Base): 
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    products = relationship("Product", back_populates="category")


class Product(Base): 
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)  
    image = Column(String)
    category_id = Column(Integer, ForeignKey("categories.id"))
    color = Column(String)
    rating = Column(Float, nullable=True)
    reviews = Column(Integer, nullable=True)
    description = Column(String, nullable=True)
    tags = Column(ARRAY(String), nullable=True)  
    created_at = Column(DateTime, default=datetime.utcnow)
    category = relationship("Category", back_populates="products")
