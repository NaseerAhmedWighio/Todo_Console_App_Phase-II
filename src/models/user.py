from datetime import datetime
from uuid import uuid4
from pydantic import BaseModel, Field, EmailStr
from pydantic.functional_validators import field_validator
import hashlib
import secrets


def hash_password(password: str) -> str:
    """Hash a password using SHA-256 with salt."""
    salt = secrets.token_hex(16)
    pwdhash = hashlib.sha256((password + salt).encode()).hexdigest()
    return f"{pwdhash}:{salt}"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    pwdhash, salt = hashed_password.split(':')
    return pwdhash == hashlib.sha256((plain_password + salt).encode()).hexdigest()


class User(BaseModel):
    """
    Represents a user with properties including ID (unique identifier),
    Username, Email, Password Hash, and Created Date
    """

    id: str = Field(
        default_factory=lambda: str(uuid4()),
        description="Unique identifier for the user",
    )
    username: str = Field(..., min_length=3, max_length=50, description="Username for the user")
    email: EmailStr = Field(..., description="Email address of the user")
    password_hash: str = Field(..., description="Hashed password")
    created_date: datetime = Field(
        default_factory=datetime.now, description="Timestamp when the user was created"
    )

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        if not v or len(v.strip()) == 0:
            raise ValueError("Username must not be empty")
        if len(v.strip()) < 3:
            raise ValueError("Username must be at least 3 characters long")
        if len(v.strip()) > 50:
            raise ValueError("Username must be no more than 50 characters long")
        # Check for valid characters (alphanumeric and underscore/hyphen)
        import re
        if not re.match(r'^[a-zA-Z0-9_-]+$', v.strip()):
            raise ValueError("Username can only contain letters, numbers, underscores, and hyphens")
        return v.strip()

    @field_validator("password_hash")
    @classmethod
    def validate_password_hash(cls, v: str) -> str:
        if not v or len(v.strip()) == 0:
            raise ValueError("Password hash must not be empty")
        # Verify it's in the format hash:salt
        parts = v.split(':')
        if len(parts) != 2 or len(parts[0]) != 64 or len(parts[1]) != 32:  # SHA-256 hash is 64 chars, salt is 32 chars
            raise ValueError("Invalid password hash format")
        return v


class UserCreate(BaseModel):
    """Model for creating new users"""

    username: str = Field(..., min_length=3, max_length=50, description="Username for the user")
    email: EmailStr = Field(..., description="Email address of the user")
    password: str = Field(..., min_length=6, description="Plain text password")

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if not v or len(v.strip()) == 0:
            raise ValueError("Password must not be empty")
        if len(v.strip()) < 6:
            raise ValueError("Password must be at least 6 characters long")
        return v.strip()


class UserLogin(BaseModel):
    """Model for user login"""

    username: str = Field(..., description="Username for login")
    password: str = Field(..., description="Plain text password for login")


class UserUpdate(BaseModel):
    """Model for updating user information"""

    username: str = Field(default=None, min_length=3, max_length=50, description="New username")
    email: EmailStr = Field(default=None, description="New email address")
    password: str = Field(default=None, min_length=6, description="New plain text password")

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if v is not None:
            if len(v.strip()) < 6:
                raise ValueError("Password must be at least 6 characters long")
        return v.strip() if v else v


class UserResponse(BaseModel):
    """Response model for API operations - excludes sensitive information"""

    id: str
    username: str
    email: str
    created_date: datetime


class AuthToken(BaseModel):
    """Authentication token model"""

    access_token: str
    token_type: str = "bearer"
    user_id: str
    username: str