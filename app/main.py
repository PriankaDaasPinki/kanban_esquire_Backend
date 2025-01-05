# app/main.py
from fastapi import FastAPI
from app.auth import auth_router
from app.users import users_router
from . import models
from app.database import engine
from app.projects import project_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()



# Include routers
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(project_router, prefix="/projects", tags=["projects"])

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI Authentication Project"}

