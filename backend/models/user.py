"""User model for Todo App backend."""
from sqlmodel import SQLModel, Field
from typing import Optional


class UserBase(SQLModel):
    """Base class for User model with common fields."""
    email: str = Field(unique=True, nullable=False)
    name: Optional[str] = Field(default=None)


class User(UserBase, table=True):
    """User model - primarily managed by Better Auth, but referenced for relations."""
    id: Optional[str] = Field(default=None, primary_key=True)  # Auto-generated string ID
    hashed_password: str = Field(max_length=255, nullable=False)  # Store hashed password