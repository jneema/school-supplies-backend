from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.categories_model import Category, Product
from app.schemas.categories_schema import CategoryCreate, ProductCreate, ProductUpdate
from fastapi import HTTPException
from datetime import datetime
from typing import List

def create_category(db: Session, category: CategoryCreate):
    db_category = Category(
        category_name=category.category_name,
        created_at=category.created_at or datetime.utcnow(),
        image_link=category.image_link,
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_all_categories(db: Session, skip: int = 0, limit: int = 100) -> List[Category]:
    try:
        stmt = select(Category).offset(skip).limit(limit)
        categories = db.execute(stmt).scalars().all()
        return categories
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to retrieve categories")

def get_category(db: Session, category_id: int) -> Category:
    try:
        category = db.get(Category, category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        return category
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to retrieve category")

def get_or_create_category(db: Session, category_name: str, image_link: str = None) -> int:
    stmt = select(Category).where(Category.category_name == category_name)
    db_category = db.execute(stmt).scalar_one_or_none()
    if not db_category:
        db_category = Category(
            category_name=category_name,
            image_link=image_link,
            created_at=datetime.utcnow(),
        )
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
    return db_category.id

def create_product(db: Session, product: ProductCreate):
    if product.category and not product.category_id:
        product.category_id = get_or_create_category(db, product.category)

    db_product = Product(
        name=product.name,
        price=product.price,
        old_price=product.old_price,
        category_id=product.category_id,
        color=product.color,
        colors=product.colors,
        rating=product.rating,
        review_count=product.review_count,
        description=product.description,
        image_link=product.image_link,
        features=product.features,
        specifications=[spec.dict() for spec in product.specifications] if product.specifications else None,
        tags=product.tags,
        in_stock=product.in_stock,
        created_at=product.created_at or datetime.utcnow(),
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_all_products(db: Session, skip: int = 0, limit: int = 100) -> List[Product]:
    try:
        stmt = select(Product).offset(skip).limit(limit)
        products = db.execute(stmt).scalars().all()
        return products
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to retrieve products")

def get_product(db: Session, product_id: int) -> Product:
    try:
        product = db.get(Product, product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to retrieve product")

def update_product(db: Session, product_id: int, product: ProductUpdate):
    db_product = db.get(Product, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    if product.category and not product.category_id:
        product.category_id = get_or_create_category(db, product.category)

    if product.price is not None:
        db_product.old_price = db_product.price

    update_data = product.dict(exclude_unset=True)
    for key, value in update_data.items():
        if key == "specifications" and value is not None:
            value = [spec.dict() for spec in value]
        setattr(db_product, key, value)

    db.commit()
    db.refresh(db_product)
    return db_product