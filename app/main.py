# app/main.py
from fastapi import FastAPI
from app.routers.auth import auth_router
from app.routers.users import users_router
from . import models
from app.database import engine
from app.routers.projects import project_router
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Add CORS middleware to handle preflight OPTIONS requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with specific domains in production
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

# Include routers
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(project_router, prefix="/projects", tags=["Projects"])

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI KANBAN Project"}

