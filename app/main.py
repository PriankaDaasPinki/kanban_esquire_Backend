# app/main.py
from fastapi import FastAPI
from app.routers.auth import auth_router
from app.routers.users import users_router
from . import models
from app.database import engine
from app.routers.projects import project_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()



# Include routers
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(project_router, prefix="/projects", tags=["Projects"])

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI Authentication Project"}

