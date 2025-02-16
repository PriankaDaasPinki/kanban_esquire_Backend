# app/projects.py
from fastapi import APIRouter, Depends, HTTPException, status, Response

from sqlalchemy.orm import Session
from app.database import get_db
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload
from app.schemas import TaskCreate, TaskUpdate, TaskResponse
from app.models import Task

task_router = APIRouter()


@task_router.get("/{module_id}", response_model=None)
async def tasks_list(module_id: int, db: Session = Depends(get_db)):
    try:
        view_tasks = (
            db.query(Task).filter(Task.module_id == module_id)
            # .options(
            #     joinedload(Task.created_by_user), joinedload(Task.assignee_user)
            # )  # Eager load related users
            .all()
        )
        # tasks_response = [TaskResponse.from_orm(task) for task in view_tasks]
        return {"status": "success", "tasks": view_tasks}
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching tasks - {e}",
        )


# @task_router.get("/{id}", response_model=None)
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


@task_router.delete("/{id}", response_model=None)
async def delete_module(id: int, db: Session = Depends(get_db)):
    try:
        task = db.query(Task).filter(Task.task_id == id)
        if task.first() == None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project with id {id} does not exit.",
            )
        delete_task = task.first()
        db.delete(task.first())
        db.commit()
        return {
            "status": f"successfully deleted task with id {delete_task.task_id}",
            "Project Module": delete_task,
            "message": f"Project {delete_task.task_name} is deleted.",
        }
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching the task - {e}",
        )


@task_router.put(
    "/update/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=TaskUpdate
)
async def update_project_module(
    id: int, module: TaskUpdate, db: Session = Depends(get_db)
):
    try:
        # Fetch the existing project
        existing_task = db.query(Task).filter(Task.task_id == id).first()

        if not existing_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with id {id} does not exist.",
            )

        # Update the attributes of the existing project
        for key, value in module.dict(exclude_unset=True).items():
            setattr(existing_task, key, value)

        # Commit changes to the database
        db.commit()
        db.refresh(existing_task)

        return existing_task

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating the task: {str(e)}",
        )


@task_router.post("/create", status_code=status.HTTP_201_CREATED, response_model=None)
async def create_module(new_task: TaskCreate, db: Session = Depends(get_db)) -> Task:
    print(new_task.dict())
    task = Task(**new_task.dict())
    db.add(task)
    db.commit()
    db.refresh(task)
    return {"status": "Created", "task": task}
