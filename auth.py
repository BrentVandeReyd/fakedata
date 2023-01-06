import crud
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status

SECRET_KEY = "14592e2e8eb49af39ecd9ab1f1263e22691b582d1a716d2415356046d39dc398"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(db: Session, username: str, password: str):
    user = crud.get_user_by_email(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict):
    to_encode = data.copy()
    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        # Default to 15 minutes of expiration time if ACCESS_TOKEN_EXPIRE_MINUTES variable is empty
        expire = datetime.utcnow() + timedelta(minutes=15)
    # Adding the JWT expiration time case
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt