from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from app.db.database import engine, sessionLocal
import app.model.models as models
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from .auth import get_current_user


router=APIRouter(prefix="/users",tags=["users"])


models.Base.metadata.create_all(bind=engine)

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserVerification(BaseModel):
    current_password: str = Field(description="Current password of the user")
    new_password: str = Field(min_length=6,description="New password of the user")

        
        
@router.get("/",status_code=status.HTTP_200_OK)
# get users who are logged in
async def get_users_logged_in(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
    return db.query(models.Users).filter(models.Users.id == user.get("id")).first()

@router.put("/password",status_code=status.HTTP_200_OK)
async def change_password(user: user_dependency, user_verification: UserVerification, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
    
    user = db.query(models.Users).filter(models.Users.id == user.get("id")).first()
    
    if not bcrypt_context.verify(user_verification.current_password,user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid authentication credentials")
    
    user.hashed_password = bcrypt_context.hash(user_verification.new_password)
    db.add(user)
    db.commit()
    return {"message": "Password changed successfully"}

