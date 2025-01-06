# app/models.py
# from pydantic import BaseModel
# from datetime import datetime
# from typing import Optional
from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime, TIMESTAMP, text
from sqlalchemy.types import String
from .database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    email = Column(String, index=True)

    def __repr__(self):
        return f"<User(user_id={self.user_id}, username='{self.username}')>"


class Project(Base):
    __tablename__ = "projects"

    project_id = Column(Integer, primary_key=True, index=True)
    project_name = Column(String, nullable=False, index=True)
    description = Column(Text, index=True)
    owner_id = Column(Integer, ForeignKey("users.user_id"), nullable=False, index=True)
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=text("now()"), index=True
    )

    def __repr__(self):
        return f"<Project(project_id={self.project_id}, project_name='{self.project_name}')>"


class Project_Module(Base):
    __tablename__ = "project_modules"

    module_id = Column(Integer, nullable=False, primary_key=True, index=True)
    module_name = Column(String, nullable=False, index=True)
    description = Column(Text, index=True)
    project_id = Column(Integer, ForeignKey("projects.project_id"), index=True)
    created_by = Column(Integer, ForeignKey("users.user_id"), index=True)

    def __repr__(self):
        return (
            f"<Project(project_id={self.module_id}, project_name='{self.module_name}')>"
        )
