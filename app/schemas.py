from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from fastapi import UploadFile, File


class User(BaseModel):
    username: str = Field(..., title="Username", min_length=3, max_length=50)
    email: Optional[EmailStr] = Field(None, title="Email Address")
    full_name: Optional[str] = Field(None, title="Full Name", max_length=100)
    disabled: Optional[bool] = Field(False, title="Is User Disabled")


class UserInDB(User):
    hashed_password: str = Field(..., title="Hashed Password")


# class UserLogin(BaseModel):
#     username_or_email: str = Field(..., title="Username or Email", max_length=50)
#     password: str = Field(..., title="User Password", min_length=8, max_length=255)


class Token(BaseModel):
    access_token: str = Field(..., title="Access Token")
    token_type: str = Field(..., title="Token Type", example="bearer")


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
