from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional
from fastapi import UploadFile, File
from datetime import datetime


class UserLogin(BaseModel):
    username: str = Field(..., title="Username or Email", max_length=50)
    password: str = Field(..., title="User Password", min_length=8, max_length=255)


class Token(BaseModel):
    access_token: str = Field(..., title="Access Token")
    token_type: str = Field(..., title="Token Type", example="bearer")


class TokenData(BaseModel):
    username: Optional[str] = Field(None, title="Username")

    class Config:
        orm_mode = True


# Users schemas
class UserCreate(BaseModel):
    username: str = Field(..., title="username", max_length=50)
    email: EmailStr = Field(..., title="User Email", max_length=100)
    phone: str = Field(
        ..., title="User Phone number", pattern=r"^\+?\d{7,15}$", max_length=15
    )  # Validates phone format
    password_hash: str = Field(..., title="user password", min_length=8, max_length=255)
    designation: Optional[str] = Field(None, title="User Designation", max_length=100)
    # user_image: Optional[Union[UploadFile, str]] = None,  # Accept file or URL
    user_image: Optional[UploadFile] = File(None, title="User Image")
    first_name: Optional[str] = Field(None, title="First Name", max_length=50)
    last_name: Optional[str] = Field(None, title="Last Name", max_length=50)

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    # username: str = Field(..., title="username", max_length=50)
    email: Optional[EmailStr] = Field(None, title="User Email", max_length=100)
    phone: Optional[str] = Field(
        None, title="User Phone number", pattern=r"^\+?\d{7,15}$", max_length=15
    )  # Validates phone format
    # password_hash: str = Field(..., title="user password", min_length=8, max_length=255)
    designation: Optional[str] = Field(None, title="User Designation", max_length=100)
    # user_image: Optional[Union[UploadFile, str]] = None,  # Accept file or URL
    user_image: Optional[UploadFile] = File(None, title="User Image")
    first_name: Optional[str] = Field(None, title="First Name", max_length=50)
    last_name: Optional[str] = Field(None, title="Last Name", max_length=50)

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    user_id: int = Field(..., title="User ID")
    name: Optional[str] = Field(None, title="User Name", max_length=100)
    email: Optional[str] = Field(None, title="User Email", max_length=255)
    role: Optional[str] = Field(
        None, title="User Role", max_length=50
    )  # Optional role field

    class Config:
        orm_mode = True
        


# Projects Schemas
class ProjectCreate(BaseModel):
    project_name: str = Field(..., title="Project Name", max_length=255)
    description: Optional[str] = Field(None, title="Project Description")
    owner_id: int = Field(..., title="Owner ID")

    class Config:
        orm_mode = True


class ProjectUpdate(BaseModel):
    project_name: Optional[str] = Field(None, title="Project Name", max_length=255)
    description: Optional[str] = Field(None, title="Project Description")
    owner_id: Optional[int] = Field(None, title="Owner ID")

    class Config:
        orm_mode = True


# Module Schemas
class ProjectModuleCreate(BaseModel):
    module_name: str = Field(..., title="Project Module Name", max_length=255)
    description: Optional[str] = Field(None, title="Project Module Description")
    project_id: int = Field(..., title="Project ID")
    created_by: int = Field(..., title="Owner ID")

    class Config:
        orm_mode = True


class ProjectModuleUpdate(BaseModel):
    module_name: Optional[str] = Field(
        None, title="Project Module Name", max_length=255
    )
    description: Optional[str] = Field(None, title="Project Module Description")
    project_id: Optional[int] = Field(None, title="Project ID")
    created_by: Optional[int] = Field(None, title="Owner ID")

    class Config:
        orm_mode = True


# Task schemas
class TaskCreate(BaseModel):
    task_name: str = Field(..., title="Task Name", max_length=255)
    description: Optional[str] = Field(None, title="Task Description")
    stage: str = Field(..., title="Task Stage", max_length=50)
    project_id: int = Field(..., title="Project ID")
    module_id: int = Field(..., title="Module ID")
    created_by: int = Field(..., title="Owner ID")
    assignee: Optional[int] = Field(None, title="Assignee ID")
    start_date: datetime = Field(..., title="Start Date")
    end_date: datetime = Field(..., title="End Date")

    @validator("end_date")
    def validate_dates(cls, end_date, values):
        start_date = values.get("start_date")
        if start_date and end_date < start_date:
            raise ValueError("End date cannot be before start date.")
        return end_date

    class Config:
        orm_mode = True


class TaskUpdate(BaseModel):
    task_name: Optional[str] = Field(None, title="Task Name", max_length=255)
    description: Optional[str] = Field(None, title="Task Description")
    stage: Optional[str] = Field(None, title="Task Stage", max_length=50)
    project_id: Optional[int] = Field(None, title="Project ID")
    module_id: Optional[int] = Field(None, title="Module ID")
    created_by: Optional[int] = Field(None, title="Owner ID")
    assignee: Optional[int] = Field(None, title="Assignee ID")
    start_date: Optional[datetime] = Field(None, title="Start Date")
    end_date: Optional[datetime] = Field(None, title="End Date")

    @validator("end_date")
    def validate_dates(cls, end_date, values):
        start_date = values.get("start_date")
        if start_date and end_date and end_date < start_date:
            raise ValueError("End date cannot be before start date.")
        return end_date

    class Config:
        orm_mode = True


class TaskResponse(BaseModel):
    task_id: int = Field(..., title="Task ID")
    task_name: str = Field(..., title="Task Name", max_length=255)
    description: Optional[str] = Field(None, title="Task Description")
    stage: str = Field(..., title="Task Stage", max_length=50)
    project_id: int = Field(..., title="Project ID")
    module_id: int = Field(..., title="Module ID")
    created_by_user: Optional[UserResponse] = Field(
        None, title="Created By User Details"
    )
    assignee_user: Optional[UserResponse] = Field(None, title="Assignee User Details")
    start_date: datetime = Field(..., title="Start Date")
    end_date: datetime = Field(..., title="End Date")

    class Config:
        orm_mode = True
        from_attributes = True  # This allows the use of from_orm method
