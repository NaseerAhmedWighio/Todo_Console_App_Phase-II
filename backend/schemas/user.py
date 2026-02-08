"""User schemas for Todo App backend."""
from sqlmodel import SQLModel
from typing import Optional
from pydantic import field_validator


class UserCreate(SQLModel):
    """Schema for creating a new user."""
    email: str
    password: str  # Will be securely hashed, allowing up to 128 characters
    name: Optional[str] = None

    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        # Bcrypt has a 72-byte limitation, so we enforce a reasonable limit
        password_bytes = v.encode('utf-8')
        if len(password_bytes) > 72:
            raise ValueError('Password must be 72 bytes or less (due to bcrypt limitation)')
        if len(v) > 50:  # Reasonable character limit
            raise ValueError('Password must be 50 characters or less')

        # Basic password validation - at least 6 characters
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters long')

        return v

    @field_validator('email')
    @classmethod
    def validate_email_format(cls, v):
        # Basic email validation
        if '@' not in v or '.' not in v.split('@')[-1]:
            raise ValueError('Invalid email format')
        return v


class UserLogin(SQLModel):
    """Schema for user login."""
    email: str
    password: str  # Will be verified against the hashed password

    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        # Bcrypt has a 72-byte limitation, so we enforce a reasonable limit
        password_bytes = v.encode('utf-8')
        if len(password_bytes) > 72:
            raise ValueError('Password must be 72 bytes or less (due to bcrypt limitation)')
        if len(v) > 50:  # Reasonable character limit
            raise ValueError('Password must be 50 characters or less')

        # Basic password validation - at least 6 characters
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters long')

        return v

    @field_validator('email')
    @classmethod
    def validate_email_format(cls, v):
        # Basic email validation
        if '@' not in v or '.' not in v.split('@')[-1]:
            raise ValueError('Invalid email format')
        return v


class UserRead(SQLModel):
    """Schema for reading user information."""
    id: str
    email: str
    name: Optional[str] = None


class Token(SQLModel):
    """Schema for authentication tokens."""
    access_token: str
    token_type: str


class TokenData(SQLModel):
    """Schema for token data."""
    user_id: str


class ErrorResponse(SQLModel):
    """Schema for error responses."""
    detail: str
    error_code: Optional[str] = None
    timestamp: Optional[str] = None