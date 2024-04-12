from typing import Annotated
from fastapi import APIRouter, Depends
from pydantic import BaseModel
import app.model.models as models
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.db.database import sessionLocal, engine

router = APIRouter()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]

class CreateUserRequest(BaseModel):
    email: str
    username: str
    first_name: str
    last_name: str
    password: str
    role: str


@router.get("/")
async def get_users(db:db_dependency):
    users = db.query(models.Users).all()
    return users

@router.post("/")
async def create_user(db:db_dependency,create_user_request: CreateUserRequest):
    create_user_model = models.Users(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        role=create_user_request.role, 
        is_active=True
    )
    
    db.add(create_user_model)
    db.commit()
    db.refresh(create_user_model)
    
    return create_user_model

@router.delete("/{username}")
async def delete_user(db:db_dependency,username:str):
    user = db.query(models.Users).filter(models.Users.username == username).first()
    if user:
        db.delete(user)
        db.commit()
        return {"message": "User deleted successfully"}
    else:
        return {"message": "User not found"}
    
@router.put("/{username}")
async def update_user(db:db_dependency,username:str,create_user_request: CreateUserRequest):
    user = db.query(models.Users).filter(models.Users.username == username).first()
    if user:
        user.email = create_user_request.email
        user.username = create_user_request.username
        user.first_name = create_user_request.first_name
        user.last_name = create_user_request.last_name
        user.hashed_password = bcrypt_context.hash(create_user_request.password)
        user.role = create_user_request.role
        db.commit()
        db.refresh(user)
        return user
    else:
        return {"message": "User not found"}