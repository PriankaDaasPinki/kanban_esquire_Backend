# app/projects.py
from fastapi import APIRouter, Depends, HTTPException, status, Response

from sqlalchemy.orm import Session
from app.database import get_db
from sqlalchemy.exc import SQLAlchemyError
from app.schemas import ProjectCreate, ProjectUpdate
from app.models import Project

project_router = APIRouter()


@project_router.get("/list", response_model=None)
async def list_projects(db: Session = Depends(get_db)):
    try:
        view_projects = db.query(Project).all()
        return {"status": "success", "projects": view_projects}
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching projects - {e}",
        )


@project_router.get("/{id}", response_model=None)
async def project_details(id: int, db: Session = Depends(get_db)) -> Project:
    try:
        project_details = db.query(Project).filter(Project.project_id == id).first()
        return {
            "status": "success",
            "projects": project_details or f"Project with id {id} is not found.",
        }
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Error fetching the project - {e}",
        )


@project_router.delete("/{id}", response_model=None)
async def delete_project(id: int, db: Session = Depends(get_db)):
    try:
        project = db.query(Project).filter(Project.project_id == id)
        if project.first() == None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project with id {id} does not exit.",
            )
        delete_project = project.first()
        db.delete(project.first())
        db.commit()
        return {
            "status": "successfully deleted project with id {delete_project.project_id}",
            "Project": delete_project,
            "message": f"Project {delete_project.project_name} is deleted.",
        }
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching the project - {e}",
        )


@project_router.put(
    "/update/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=ProjectUpdate
)
async def update_project(
    id: int, project: ProjectUpdate, db: Session = Depends(get_db)
):
    try:
        # Fetch the existing project
        existing_project = db.query(Project).filter(Project.project_id == id).first()

        if not existing_project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project with id {id} does not exist.",
            )

        # Update the attributes of the existing project
        for key, value in project.dict(exclude_unset=True).items():
            setattr(existing_project, key, value)

        # Commit changes to the database
        db.commit()
        db.refresh(existing_project)

        return existing_project

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating the project: {str(e)}",
        )


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
    return {"status": "Created", "project": project}
