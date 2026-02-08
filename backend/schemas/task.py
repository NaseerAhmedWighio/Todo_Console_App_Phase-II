"""Task schemas for Todo App backend."""
from sqlmodel import SQLModel
from typing import Optional
from datetime import datetime


class TaskBase(SQLModel):
    """Base schema for task operations."""
    title: str
    description: Optional[str] = None
    completed: bool = False


class TaskCreate(TaskBase):
    """Schema for creating a new task."""
    pass


class TaskRead(TaskBase):
    """Schema for reading a task with additional fields."""
    id: int
    user_id: str
    created_at: datetime
    updated_at: datetime


class TaskUpdate(SQLModel):
    """Schema for updating an existing task."""
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


class TaskComplete(SQLModel):
    """Schema for updating task completion status."""
    completed: bool


class TaskListResponse(SQLModel):
    """Schema for task list response."""
    tasks: list[TaskRead]
    total: int