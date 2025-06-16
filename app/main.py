import cloudinary
import cloudinary.uploader
import cloudinary.api
import logging
import uuid
from cloudinary import CloudinaryImage
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import inspect
from app.schemas.users_schema import UserCreate, UserResponse
from app.schemas.categories_schema import CategoryCreate, CategoryResponse, ProductCreate, ProductResponse, ProductUpdate
from app.schemas.image_schema import ImageResponse
from app.users import create_user
from app.categories import create_category, create_product, update_product
from app.database import engine, SessionLocal, Base
from app.models.image_model import Image

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


# New upload-image endpoint (no product relation)
@app.post("/upload-image/", response_model=ImageResponse)
async def upload_image(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        # Validate file type
        if not file.content_type.startswith("image/"):
            logger.error(f"Invalid file type uploaded: {file.content_type}")
            raise HTTPException(status_code=400, detail="File must be an image")

        # Generate a unique public ID
        unique_id = str(uuid.uuid4())
        public_id = f"uploads/{unique_id}_{file.filename}"

        # Upload image to Cloudinary
        upload_result = cloudinary.uploader.upload(
            file.file,
            folder="uploads",  # Store in 'uploads' folder in Cloudinary
            public_id=public_id,
            unique_filename=False,
            overwrite=True
        )

        # Get the secure URL
        image_url = upload_result.get("secure_url")
        if not image_url:
            logger.error("Failed to retrieve image URL from Cloudinary")
            raise HTTPException(status_code=500, detail="Failed to upload image")

        # Save to database
        db_image = Image(image_url=image_url, public_id=public_id)
        db.add(db_image)
        db.commit()
        db.refresh(db_image)

        logger.info(f"Image uploaded successfully: {image_url}")
        return db_image

    except Exception as e:
        logger.error(f"Error uploading image: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error uploading image: {str(e)}")