from datetime import datetime, timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
import app.model.models as models
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.db.database import sessionLocal, engine
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt

router = APIRouter(prefix="/auth",tags=["auth"])

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

SECRETKEY = "f4b3b3c4-4b4b-4b4b-8b4b"
ALGORITH = "HS256"



models.Base.metadata.create_all(bind=engine)

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]

def is_user_authenticated(username:str,password:str,db:Session):
    user = db.query(models.Users).filter(models.Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password,user.hashed_password):
        return False
    return user

def create_access_token(username: str, user_id:int, role: str, expires_delta: timedelta):
    to_encode = {"sub": username, "user_id": user_id, "role": role}
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRETKEY, algorithm=ALGORITH)
    return encoded_jwt

def get_current_user(token: Annotated[str,Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRETKEY, algorithms=[ALGORITH])
        username: str = payload.get("sub")
        userid = payload.get("user_id")
        user_role = payload.get("role")
        if username is not None:
            return {"username": username, "id": userid, "user_role": user_role}
    except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")

class CreateUserRequest(BaseModel):
    email: str
    username: str
    first_name: str
    last_name: str
    password: str
    role: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "user1@gmail.com",
                "username": "user1",
                "first_name": "user1",
                "last_name": "user1",
                "password": "test1234",
                "role": "devops"
            }
        }
    
class Token(BaseModel):
    access_token: str
    token_type: str


@router.get("/")
async def get_users(db:db_dependency):
    users = db.query(models.Users).all()
    return users

@router.post("/", description="Create a new user")
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
    print("User from delete auth route: ", user)
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
    
    
@router.post("/token", response_model=Token, description="Login for access token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],db:db_dependency):
    user = is_user_authenticated(form_data.username,form_data.password,db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
    
    user_token = create_access_token(form_data.username,user.id,user.role,timedelta(minutes=30))
    return {"access_token": user_token, "token_type": "bearer"}