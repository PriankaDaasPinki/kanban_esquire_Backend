# app/models.py
from sqlalchemy import Column, Integer, Text, ForeignKey, TIMESTAMP, text, LargeBinary
from sqlalchemy.types import String
from .database import Base
from sqlalchemy.orm import validates, relationship


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True, index=True)
    first_name = Column(String(50), nullable=False, server_default="", index=True)
    last_name = Column(String(50), nullable=False, server_default="", index=True)
    email = Column(String(100), nullable=False, unique=True, index=True)
    phone = Column(String(15), nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    designation = Column(String(100), index=True)
    user_image = Column(
        LargeBinary, index=True
    )  # For image binary data, use LargeBinary
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=text("now()"), index=True
    )

    def __repr__(self):
        return f"<User(user_id={self.user_id}, username='{self.username}')>"


class Project(Base):
    __tablename__ = "projects"

    project_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
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

    module_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    module_name = Column(String, nullable=False, index=True)
    description = Column(Text, index=True)
    project_id = Column(Integer, ForeignKey("projects.project_id"), index=True)
    created_by = Column(Integer, ForeignKey("users.user_id"), index=True)

    def __repr__(self):
        return (
            f"<Project Module(project_module_id={self.module_id}, Module_name='{self.module_name}')>"
        )
        
        
class Task(Base):
    __tablename__ = "tasks"

    task_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    task_name = Column(String, nullable=False, index=True)
    description = Column(Text, index=True)
    stage = Column(String, nullable=False, index=True)
    project_id = Column(Integer, ForeignKey("projects.project_id"), index=True)
    module_id = Column(Integer, ForeignKey("project_modules.module_id"), index=True)
    created_by = Column(Integer, ForeignKey("users.user_id"), index=True)
    assignee = Column(Integer, ForeignKey("users.user_id"), index=True)
    start_date = Column(TIMESTAMP(timezone=True), nullable=False, index=True)
    end_date = Column(TIMESTAMP(timezone=True), nullable=False, index=True)

    # Relationships to fetch user details
    created_by_user = relationship("User", foreign_keys=[created_by])
    assignee_user = relationship("User", foreign_keys=[assignee])

    @validates("start_date", "end_date")
    def validate_dates(self, key, value):
        """Ensures start_date is before end_date"""
        if key == "start_date":
            end_date = self.__dict__.get("end_date")  # Fetch from instance dictionary
            if end_date and value > end_date:
                raise ValueError("Start date cannot be after the end date.")
        elif key == "end_date":
            start_date = self.__dict__.get("start_date")
            if start_date and value < start_date:
                raise ValueError("End date cannot be before the start date.")
        return value

    def __repr__(self):
        return f"<Task(task_id={self.task_id}, task_name='{self.task_name}')>"
