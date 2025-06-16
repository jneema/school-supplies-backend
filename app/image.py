# app/images.py
import cloudinary.uploader
import logging
from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
from app.models.image_model import Image
from app.models.users_model import User
from app.models.categories_model import Product, Category
import uuid
from typing import Optional, List

logger = logging.getLogger(__name__)

async def create_images(
    db: Session,
    files: List[UploadFile],
    user_id: Optional[int] = None,
    product_id: Optional[int] = None,
    category_id: Optional[int] = None
) -> List[Image]:
    try:
        # Validate that only one ID is provided
        provided_ids = sum(1 for id in [user_id, product_id, category_id] if id is not None)
        if provided_ids > 1:
            logger.error("Multiple entity IDs provided; only one allowed")
            raise HTTPException(status_code=400, detail="Provide only one of user_id, product_id, or category_id")

        # Validate entity existence
        if user_id:
            if not db.query(User).filter(User.id == user_id).first():
                logger.error(f"User with ID {user_id} not found")
                raise HTTPException(status_code=404, detail="User not found")
        elif product_id:
            if not db.query(Product).filter(Product.id == product_id).first():
                logger.error(f"Product with ID {product_id} not found")
                raise HTTPException(status_code=404, detail="Product not found")
        elif category_id:
            if not db.query(Category).filter(Category.id == category_id).first():
                logger.error(f"Category with ID {category_id} not found")
                raise HTTPException(status_code=404, detail="Category not found")

        uploaded_images = []
        folder = "uploads"
        if user_id:
            folder = f"users/{user_id}"
        elif product_id:
            folder = f"products/{product_id}"
        elif category_id:
            folder = f"categories/{category_id}"

        for file in files:
            if not file.content_type.startswith("image/"):
                logger.error(f"Invalid file type uploaded: {file.content_type}")
                raise HTTPException(status_code=400, detail=f"File {file.filename} must be an image")

            unique_id = str(uuid.uuid4())
            public_id = f"{folder}/{unique_id}_{file.filename}"

            upload_result = cloudinary.uploader.upload(
                file.file,
                folder=folder,
                public_id=public_id,
                unique_filename=False,
                overwrite=True
            )

            image_url = upload_result.get("secure_url")
            if not image_url:
                logger.error(f"Failed to retrieve image URL for {file.filename}")
                raise HTTPException(status_code=500, detail=f"Failed to upload {file.filename}")

            db_image = Image(
                image_url=image_url,
                public_id=public_id,
                user_id=user_id,
                product_id=product_id,
                category_id=category_id
            )
            db.add(db_image)
            uploaded_images.append(db_image)

        db.commit()
        for db_image in uploaded_images:
            db.refresh(db_image)

        logger.info(f"Uploaded {len(uploaded_images)} images successfully")
        return uploaded_images

    except Exception as e:
        logger.error(f"Error uploading images: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error uploading images: {str(e)}")