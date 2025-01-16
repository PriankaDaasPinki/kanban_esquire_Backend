# app/auth.py
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session

# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta, datetime
from jose import JWTError, jwt
from app.schemas import Token, UserLogin
from app.dependencies import get_user, authenticate_user, create_access_token, verify_access_token

from app.database import get_db


auth_router = APIRouter()



@auth_router.post("/login")
async def login(user_credintials: UserLogin, db: Session = Depends(get_db)):
    print("user_credintials", user_credintials)
    user = get_user(user_credintials.username, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with username or email {user_credintials.username} not found",
        )

    verified_user = authenticate_user(user, user_credintials.password)
    if not verified_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password"
        )

    token = create_access_token(data={"username": user.username})

    return {
        "message": "Login to get access token",
        "token": token,
        "token_type": "bearer",
        "user": user,
    }


# @auth_router.post("/token", response_model=Token)
# async def login(
#     form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
# ):

#     user = authenticate_user(get_user(form_data.username, db), form_data.password)
#     print(user.username)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.username},
#         expires_delta=access_token_expires,
#         secret=SECRET_KEY,
#         ALGORITHM=ALGORITHM,
#     )
#     return {"access_token": access_token, "token_type": "bearer"}


@auth_router.get("/validate-token")
async def validate_token(token: str):
    try:
        payload = verify_access_token(token, credentials_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"))
        # payload = jwt.decode(token)
        return {"valid": True, "details": payload}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
