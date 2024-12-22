from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from sqlalchemy.orm import Session
from database import session_local
from pydantic import BaseModel
from models import Users
from passlib.context import CryptContext
from starlette import status
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

router = APIRouter(
    prefix="/auth",
    tags=['auth']
)

SECRET_KEY = '4032c0a3341f4eba82b524d1b22bf7fa024ca717e5365ec2f7da2d8096660677'
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/login')

class CreateUserRequest(BaseModel):
    name: str
    email: str
    password: str
    role:str

class LoginUserRequest(BaseModel):
    email: str
    password: str

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

def authenticate_user(email:str, password: str, db):
    user = db.query(Users).filter(Users.email == email).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(email:str, user_id:int, hours:int=8):
    payload = {
        "sub":email,
        "id": user_id,
        "iat":datetime.now(timezone.utc),
        "exp":datetime.now(timezone.utc) + timedelta(hours=hours)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token:Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token=token, SECRET_KEY=SECRET_KEY, algorithms=[ALGORITHM])
        email:str = payload.get('sub')
        user_id: int = payload.get('id')
        if email is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid user')
        return {'email':email, 'id':user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid user')


@router.post("/user", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, user_request:CreateUserRequest):
    create_user_model = Users(
        name= user_request.name,
        email = user_request.email,
        hashed_password =bcrypt_context.hash(user_request.password),
        is_active = True,
        role = user_request.role
    )
    db.add(create_user_model)
    db.commit()

@router.post("/login",status_code=status.HTTP_200_OK)
async def user_login(db: db_dependency, user_request:LoginUserRequest):
    user = authenticate_user(email=user_request.email, password=user_request.password, db=db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid user')
    token = create_access_token(user.email, user.id)
    return token