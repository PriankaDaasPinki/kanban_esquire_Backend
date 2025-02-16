# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.auth import auth_router
from app.routers.users import users_router
from . import models
from app.database import engine
from app.routers.projects import project_router
from app.routers.project_module import project_module_router
from app.routers.tasks import task_router
# import uvicorn

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# if __name__ == "main":
#     uvicorn.run(app, host="10.20.1.80", port=8000)

# Add CORS middleware to handle preflight OPTIONS requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with specific domains in production
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)
# Define your allowed origins (domains)
allowed_origins = [
    "10.20.1.80",
    "*",
    # "*" can be used to allow all origins (not recommended for production)
    # "*"
]

# Include routers
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(project_router, prefix="/projects", tags=["Projects"])
app.include_router(project_module_router, prefix="/project_module", tags=["Project Modules"])
app.include_router(task_router, prefix="/tasks", tags=["Tasks"])


@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI KANBAN Project"}
