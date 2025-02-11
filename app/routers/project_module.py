# app/projects.py
from fastapi import APIRouter, Depends, HTTPException, status, Response

from sqlalchemy.orm import Session
from app.database import get_db
from sqlalchemy.exc import SQLAlchemyError
from app.schemas import ProjectModuleCreate, ProjectUpdate
from app.models import Project_Module

project_module_router = APIRouter()


@project_module_router.get("/{id}", response_model=None)
async def list_project_module(id: int, db: Session = Depends(get_db)):
    try:
        view_project_module = (
            db.query(Project_Module).filter(Project_Module.project_id == id).all()
        )
        # project_details = db.query(Project).filter(Project.project_id == id).first()
        print("view project module", view_project_module)

        return {"status": "success", "project_modules": view_project_module}
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching project modules - {e}",
        )


# @project_module_router.get("/{id}", response_model=None)
# async def project_details(id: int, db: Session = Depends(get_db)) -> Project:
#     try:
#         project_details = db.query(Project).filter(Project.project_id == id).first()
#         return {
#             "status": "success",
#             "projects": project_details or f"Project with id {id} is not found.",
#         }
#     except SQLAlchemyError as e:
#         print('e',e)
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Error fetching the project - {e}",
#         )


@project_module_router.delete("/{id}", response_model=None)
async def delete_module(id: int, db: Session = Depends(get_db)):
    try:
        module = db.query(Project_Module).filter(Project_Module.module_id == id)
        if module.first() == None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project with id {id} does not exit.",
            )
        delete_module = module.first()
        db.delete(module.first())
        db.commit()
        return {
            "status": f"successfully deleted project module with id {delete_module.module_id}",
            "Project Module": delete_module,
            "message": f"Project {delete_module.module_name_name} is deleted.",
        }
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching the project - {e}",
        )


# @project_module_router.put(
#     "/update/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=ProjectUpdate
# )
# async def update_project(
#     id: int, project: ProjectUpdate, db: Session = Depends(get_db)
# ):
#     try:
#         # Fetch the existing project
#         existing_project = db.query(Project).filter(Project.project_id == id).first()

#         if not existing_project:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail=f"Project with id {id} does not exist.",
#             )

#         # Update the attributes of the existing project
#         for key, value in project.dict(exclude_unset=True).items():
#             setattr(existing_project, key, value)

#         # Commit changes to the database
#         db.commit()
#         db.refresh(existing_project)

#         return existing_project

#     except SQLAlchemyError as e:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Error updating the project: {str(e)}",
#         )


@project_module_router.post(
    "/create", status_code=status.HTTP_201_CREATED, response_model=None
)
async def create_module(
    new_module: ProjectModuleCreate, db: Session = Depends(get_db)
) -> Project_Module:
    print(new_module.dict())
    module = Project_Module(**new_module.dict())
    db.add(module)
    db.commit()
    db.refresh(module)  # Refresh to get the auto-generated fields like `project_id`
    return {"status": "Created", "project_module": module}
