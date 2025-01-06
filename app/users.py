# app/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from app.models import User
from sqlalchemy.orm import Session
from app.dependencies import get_current_active_user
from app.database import get_db
from sqlalchemy.exc import SQLAlchemyError

users_router = APIRouter()

@users_router.get("/me", response_model=None)
async def read_current_user(current_user: User = Depends(get_current_active_user)):
    return current_user


@users_router.get("/")
async def list_users(db: Session = Depends(get_db)):
    try:
        All_Users = db.query(User).all()
        return {"status": "success", "Users": All_Users}
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching Users.",
        )
    # return [{"username": "johndoe", "full_name": "John Doe"}]

