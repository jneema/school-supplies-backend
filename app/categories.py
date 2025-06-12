from sqlalchemy.orm import Session
from app.models.categories_model import Category, Product
from app.schemas.categories_schema import CategoryCreate, ProductCreate

def create_category(db: Session, category: CategoryCreate):
    db_category = Category(
        category_name=category.category_name,
        created_at=category.created_at,
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def create_product(db: Session, product: ProductCreate):
    db_product = Product(
        name=product.name,
        price=product.price,
        image=product.image,
        category_id=product.category_id,
        color=product.color,
        rating=product.rating,
        reviews=product.reviews,
        description=product.description,
        tags=product.tags,
        created_at=product.created_at,
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product
