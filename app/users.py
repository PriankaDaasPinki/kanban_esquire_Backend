# app/users.py
from fastapi import APIRouter, Depends, HTTPException
from app.models import User
from app.dependencies import get_current_active_user

users_router = APIRouter()

@users_router.get("/me", response_model=User)
async def read_current_user(current_user: User = Depends(get_current_active_user)):
    return current_user

@users_router.get("/")
async def list_users():
    return [{"username": "johndoe", "full_name": "John Doe"}]
