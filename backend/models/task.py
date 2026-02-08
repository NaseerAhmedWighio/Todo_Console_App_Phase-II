"""Task model for Todo App backend."""
from sqlmodel import SQLModel, Field, Column, DateTime
from typing import Optional
from datetime import datetime


class TaskBase(SQLModel):
    """Base class for Task model with common fields."""
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)


class Task(TaskBase, table=True):
    """Task model representing a user's todo item."""
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)  # Links to Better Auth user ID
    created_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime(timezone=True)))
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime(timezone=True)))