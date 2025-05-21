from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from . import models, schemas, users
from .database import engine, SessionLocal, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="User Management API", version="1.0")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = users.create_user(db=db, user=user)
    return db_user
