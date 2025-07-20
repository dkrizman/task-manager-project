from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum


class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, description="Task title")
    description: Optional[str] = Field(None, description="Task description")
    priority: Priority = Field(Priority.MEDIUM, description="Task priority")


class TaskCreate(TaskBase):
    """Schema for creating a new task"""
    pass


class TaskUpdate(BaseModel):
    """Schema for updating a task"""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[Priority] = None


class TaskResponse(TaskBase):
    """Schema for task response"""
    id: int
    completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TaskList(BaseModel):
    """Schema for paginated task list"""
    tasks: list[TaskResponse]
    total: int
    page: int
    size: int
    pages: int