from datetime import datetime
from uuid import uuid4
from pydantic import BaseModel, Field
from pydantic.functional_validators import field_validator


class Task(BaseModel):
    """
    Represents a single todo item with properties including ID (unique identifier),
    Description (text content), Status (Complete/Incomplete), Created Date (timestamp)
    """

    id: str = Field(
        default_factory=lambda: str(uuid4()),
        description="Unique identifier for the task",
    )
    description: str = Field(..., min_length=1, description="Text content of the task")
    status: str = Field(
        default="incomplete",
        pattern=r"^(incomplete|complete)$",
        description="Current status of the task",
    )
    created_date: datetime = Field(
        default_factory=datetime.now, description="Timestamp when the task was created"
    )

    @field_validator("description")
    @classmethod
    def validate_description(cls, v: str) -> str:
        if not v or len(v.strip()) == 0:
            raise ValueError("Description must not be empty")
        return v.strip()

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str) -> str:
        if v not in ["incomplete", "complete"]:
            raise ValueError('Status must be either "incomplete" or "complete"')
        return v

    @field_validator("created_date")
    @classmethod
    def validate_created_date(cls, v: datetime) -> datetime:
        if v > datetime.now():
            raise ValueError("Created date must be in the past or present")
        return v


class TaskCreate(BaseModel):
    """Model for creating new tasks"""

    description: str = Field(..., min_length=1, description="The task description")


class TaskUpdate(BaseModel):
    """Model for updating existing tasks"""

    description: str = Field(
        ..., min_length=1, description="The updated task description"
    )


class TaskStatusUpdate(BaseModel):
    """Model for updating task status"""

    status: str = Field(
        ...,
        pattern=r"^(incomplete|complete)$",
        description="The new status for the task",
    )


class TaskResponse(Task):
    """Response model for API operations - extends base Task model"""

    pass
