# app/projects.py
from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Project

project_router = APIRouter()


@project_router.get("/projects")
async def list_project(db: Session = Depends(get_db)):
    view_projects = db.query(Project).all()
    return {"status": "success", "projects": view_projects}


@project_router.post(
    "/projects", status_code=status.HTTP_201_CREATED, response_model=None
)
async def create_project(
    new_project: Project, db: Session = Depends(get_db)
) -> Project:
    print(new_project.dict())
    return {"status": "success", "projects": "create_projects"}
