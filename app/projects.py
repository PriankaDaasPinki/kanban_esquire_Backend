# app/projects.py
from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session
from app.database import get_db
from sqlalchemy.exc import SQLAlchemyError
from app.schemas import ProjectCreate
from app.models import Project

project_router = APIRouter()


@project_router.get("/")
async def list_projects(db: Session = Depends(get_db)):
    try:
        view_projects = db.query(Project).all()
        return {"status": "success", "projects": view_projects}
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching projects.",
        )


# @project_router.post(
#     "/", status_code=status.HTTP_201_CREATED, response_model=ProjectSchema
# )
# async def create_project(
#     new_project: ProjectSchema, db: Session = Depends(get_db)
# ) -> ProjectSchema:
#     # Convert Pydantic model to SQLAlchemy model
#     # project = Project(**new_project.dict())
#     # db.add(project)
#     # db.commit()
#     # db.refresh(project)  # Refresh to get the auto-generated fields like `project_id`
#     print(new_project.dict())
#     return "project"


@project_router.post(
    "/create", status_code=status.HTTP_201_CREATED, response_model=None
)
async def create_project(
    new_project: ProjectCreate, db: Session = Depends(get_db)
) -> Project:
    print(new_project.dict())
    project = Project(**new_project.dict())
    db.add(project)
    db.commit()
    db.refresh(project)  # Refresh to get the auto-generated fields like `project_id`
    return {"status": "success", "projects": project, "Created": "Successfully"}
