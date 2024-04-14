from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from app.db.database import engine, sessionLocal
import app.model.models as models
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from app.db.curd import get_server_by_hostname
from .auth import get_current_user


router=APIRouter(prefix="/admin",tags=["admin"])


models.Base.metadata.create_all(bind=engine)

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get("/inventory",status_code=status.HTTP_200_OK)
async def get_all_servers(user: user_dependency, db: db_dependency):
    if user is None or user.get("user_role") != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
    return db.query(models.Servers).all()
    
