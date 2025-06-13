import cloudinary
import cloudinary.uploader
import json
import logging
import os
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import inspect
from typing import Optional
from app.schemas.users_schema import UserCreate, UserResponse
from app.schemas.categories_schema import CategoryCreate, CategoryResponse, ProductCreate, ProductResponse, ProductUpdate
from app.users import create_user
from app.categories import create_category, create_product, update_product
from app.database import engine, SessionLocal, Base


load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
API_KEY = os.getenv("CLOUDINARY_API_KEY")
API_SECRET = os.getenv("CLOUDINARY_API_SECRET")

if not all([CLOUD_NAME, API_KEY, API_SECRET]):
    missing = [k for k, v in [("CLOUDINARY_CLOUD_NAME", CLOUD_NAME), 
                             ("CLOUDINARY_API_KEY", API_KEY), 
                             ("CLOUDINARY_API_SECRET", API_SECRET)] if not v]
    raise ValueError(f"Missing Cloudinary environment variables: {missing}")

cloudinary.config(
    cloud_name=CLOUD_NAME,
    api_key=API_KEY,
    api_secret=API_SECRET
)
logger.info(f"Cloudinary configured with cloud_name: {CLOUD_NAME}")

try:
    Base.metadata.create_all(bind=engine)
    inspector = inspect(engine)
    if 'categories' in inspector.get_table_names() and 'products' in inspector.get_table_names():
        logger.info("Database tables 'categories' and 'products' verified/created successfully")
    else:
        logger.error("Database tables not found after creation attempt")
        raise Exception("Table creation failed")
except Exception as e:
    logger.error(f"Failed to create/verify database tables: {str(e)}")
    raise

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db=db, user=user)

@app.post("/categories/", response_model=CategoryResponse)
def add_category(category: CategoryCreate, db: Session = Depends(get_db)):
    return create_category(db=db, category=category)

@app.post("/products/", response_model=ProductResponse)
def add_product(product: ProductCreate, db: Session = Depends(get_db)):
    return create_product(db=db, product=product)

@app.put("/products/{id}", response_model=ProductResponse)
def update_product_endpoint(
    id: int,
    product: ProductUpdate,
    db: Session = Depends(get_db)
):
    return update_product(db=db, product_id=id, product=product)