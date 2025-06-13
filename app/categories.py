from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.categories_model import Category, Product
from app.schemas.categories_schema import CategoryCreate, ProductCreate, ProductUpdate
from fastapi import HTTPException
from datetime import datetime

def create_category(db: Session, category: CategoryCreate):
    db_category = Category(
        category_name=category.category_name,
        created_at=category.created_at or datetime.utcnow(),
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_or_create_category(db: Session, category_name: str) -> int:
    stmt = select(Category).where(Category.category_name == category_name)
    db_category = db.execute(stmt).scalar_one_or_none()
    if not db_category:
        db_category = Category(
            category_name=category_name,
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