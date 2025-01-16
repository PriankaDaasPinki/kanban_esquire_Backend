# app/dependencies.py
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timedelta
from sqlalchemy import or_

from app.models import User
from app.schemas import TokenData  # Add this import if TokenData is defined in schemas
from sqlalchemy.orm import Session
from app.database import get_db


SECRET_KEY = "KANBAN"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Password hashing utility
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_user(username: str, db: Session):
    user = (
        db.query(User)
        .filter(or_(User.username == username, User.email == username))
        .first()
    )
    return user


def authenticate_user(user: User, password: str):
    if not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    return user


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)

    except JWTError:
        raise credentials_exception
    
    return token_data


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)): # Add db: Session = Depends(get_db) if you are using SQLAlchemy
    credentials_exception = HTTPException(status_code=401, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    
    token = verify_access_token(token, credentials_exception)
    
    user = get_user(token.username, db)
    if user is None:
        raise credentials_exception
    return user



    # try:
    #     payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    #     username: str = payload.get("sub")
    #     if username is None:
    #         raise HTTPException(
    #             status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
    #         )
    # except JWTError:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
    #     )
    # user = get_user(username, db)
    # if user is None:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
    #     )
    # return user


# async def get_current_active_user(current_user: User = Depends(get_current_user)):
#     if current_user.disabled:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
#         )
#     return current_user
