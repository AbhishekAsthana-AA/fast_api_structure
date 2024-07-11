from fastapi import Depends, HTTPException,status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jwt.exceptions import InvalidTokenError
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from database.db import get_db
from models.loginmodel import LoginDetails, UserDetails
from sqlalchemy import and_
from datetime import datetime, timedelta, timezone
from typing import Union
import jwt


SECRET_KEY = "Alu"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# faltu code
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password) 

# faltu code
def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(db: Session , email_address: str, password: str):
    user = db.query(LoginDetails).filter(and_(LoginDetails.email_address == email_address,
                                              LoginDetails.password == password)).first()
    if not user:
       raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
       data={"sub": user.email_address},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
   
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    user = get_user_by_username(db, username)
    if user is None:
        raise credentials_exception
    return user

def get_user_by_username(db: Session, username: str):
    return db.query(UserDetails).filter(UserDetails.email_address == username).first()

