# app/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import base64

from app.models import User
from app.schemas import UserCreate, UserUpdate
# from app.dependencies import get_current_active_user
from app.database import get_db
from app.utils import hash_password

users_router = APIRouter()


# @users_router.get("/me", response_model=None)
# async def read_current_user(current_user: User = Depends(get_current_active_user)):
#     return current_user


@users_router.get("/list", response_model=None)
async def list_users(db: Session = Depends(get_db)):
    try:
        All_Users = db.query(User).all()
        return {"status": "success", "Users": All_Users}
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching Users.",
        )


@users_router.get("/{id}", response_model=None)
async def user_details(id: int, db: Session = Depends(get_db)) -> User:
    try:
        user_details = db.query(User).filter(User.user_id == id).first()
        return {
            "status": "success",
            "user": user_details or f"User with id {id} is not found.",
        }
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Error fetching the project - {e}",
        )


@users_router.delete("/{id}", response_model=None)
async def delete_user(id: int, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.user_id == id)
        if user.first() == None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {id} does not exit.",
            )
        delete_user = user.first()
        db.delete(user.first())
        db.commit()
        return {
            "status": f"successfully deleted user with id {delete_user.user_id}",
            "User": delete_user,
            "message": f"User {delete_user.username} is deleted.",
        }
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching the project - {e}",
        )


@users_router.put(
    "/update/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=UserUpdate
)
async def update_user(
    id: int, user: UserUpdate, db: Session = Depends(get_db)
):
    try:
        # Fetch the existing user
        existing_user = db.query(User).filter(User.user_id == id).first()

        if not existing_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {id} does not exist.",
            )

        # Update the attributes of the existing project
        for key, value in user.dict(exclude_unset=True).items():
            setattr(existing_user, key, value)

        # Commit changes to the database
        db.commit()
        db.refresh(existing_user)

        return existing_user

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating the user: {str(e)}",
        )


@users_router.post("/create", status_code=status.HTTP_201_CREATED, response_model=None)
async def create_user(new_user: UserCreate, db: Session = Depends(get_db)) -> dict:
    # Process user image
    # user_image_binary = None
    # if new_user.user_image:
    #     try:
    #         # Read the binary content of the uploaded file
    #         user_image_binary = await new_user.user_image.read()
    #     except Exception as e:
    #         raise HTTPException(status_code=400, detail="Failed to process user image")

    # Hash the password
    hashed_password = hash_password(new_user.password_hash)
    new_user.password_hash = hashed_password

    # Create the User instance
    user = User(**new_user.dict())

    try:
        # Save the user in the database
        db.add(user)
        db.commit()
        db.refresh(user)  # Refresh to get the auto-generated fields like `user_id`
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error saving user to the database - {str(e)}",
        )

    # Return a success response without including binary data
    return {
        "status": "User created successfully!",
        "user": {
            "user_id": user.user_id,
            "username": user.username,
            "email": user.email,
            "phone": user.phone,
            "designation": user.designation,
            "Name": user.first_name + " " + user.last_name,
        },
    }
