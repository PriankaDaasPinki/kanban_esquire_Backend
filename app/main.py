# app/main.py
from fastapi import FastAPI
from app.auth import auth_router
from app.users import users_router

app = FastAPI()

# Include routers
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(users_router, prefix="/users", tags=["users"])

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI Authentication Project"}

