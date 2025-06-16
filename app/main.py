import cloudinary
import logging
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import inspect
from typing import Optional, List
from app.schemas.users_schema import UserCreate, UserResponse
from app.schemas.categories_schema import CategoryCreate, CategoryResponse, ProductCreate, ProductResponse, ProductUpdate
from app.schemas.image_schema import ImageResponse
from app.users import create_user
from app.categories import create_category, create_product, update_product
from app.image import create_single_image, create_multiple_images
from app.database import engine, SessionLocal, Base

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

config = cloudinary.config(secure=True)

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

@app.post("/upload-image/single/", response_model=ImageResponse)
async def upload_single_image(
    file: UploadFile = File(...),
    user_id: Optional[int] = None,
    category_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    return await create_single_image(
    db=db,
    file=file,
    user_id=user_id,
    category_id=category_id,
)

@app.post("/upload-image/multiple/", response_model=List[ImageResponse])
async def upload_multiple_images(
    files: List[UploadFile] = File(...),
    product_id: int = None,
    db: Session = Depends(get_db)
):
    return await create_multiple_images(
        db=db,
        files=files,
        product_id=product_id
    )