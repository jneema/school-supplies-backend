# app/images.py
import cloudinary.uploader
import logging
from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
from app.models.image_model import Image
import uuid

logger = logging.getLogger(__name__)

async def create_image(db: Session, file: UploadFile) -> Image:
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