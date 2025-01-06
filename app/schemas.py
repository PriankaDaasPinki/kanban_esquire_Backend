from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(User):
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class ProjectCreate(BaseModel):
    project_name: str = Field(..., title="Project Name", max_length=255)
    description: Optional[str] = Field(None, title="Project Description")
    owner_id: int = Field(..., title="Owner ID")

    class Config:
        orm_mode = True
