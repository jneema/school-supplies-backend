from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.schemas.users_schema import UserCreate, UserResponse
from app.schemas.categories_schema import CategoryCreate, CategoryResponse, ProductCreate, ProductResponse
from app.users import create_user
from app.categories import create_category, create_product
from app.database import engine, SessionLocal, Base

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

