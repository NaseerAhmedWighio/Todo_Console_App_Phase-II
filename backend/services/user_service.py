"""User service for Todo App backend."""
from sqlmodel import Session, select
from typing import Optional
from models.user import User
from models.task import Task
from schemas.user import UserCreate, UserRead
from core.jwt import get_password_hash, verify_password
from core.logging import log_user_action
from fastapi import HTTPException, status


class UserService:
    """Service class for user-related operations."""

    def __init__(self, session: Session):
        """Initialize with database session."""
        self.session = session

    def get_user_by_id(self, user_id: str) -> Optional[UserRead]:
        """Get a user by ID."""
        user = self.session.get(User, user_id)
        if not user:
            return None
        return UserRead(id=user.id, email=user.email, name=user.name)

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get a user by email."""
        statement = select(User).where(User.email == email)
        user = self.session.exec(statement).first()
        return user

    def create_user(self, user_data: UserCreate) -> UserRead:
        """Create a new user."""
        # Check if user already exists
        existing_user = self.get_user_by_email(user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        try:
            # Hash the password - Better Auth handles password validation, not backend
            # The get_password_hash function handles the 72-byte bcrypt limitation
            hashed_password = get_password_hash(user_data.password)
        except ValueError as e:
            # Handle password hashing errors (like bcrypt issues)
            # Provide more user-friendly message
            error_message = str(e)
            if "Password too long" in error_message:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Password is too long. Please use a shorter password (less than 72 bytes)."
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Password could not be processed: {str(e)}"
                )
        except Exception as e:
            # Handle any other unexpected errors
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password processing failed. Please try a different password."
            )

        # Use the user ID from Better Auth if provided, otherwise generate one
        import uuid
        user_id = f"user_{uuid.uuid4().hex}"

        # Create user with auto-generated ID and store hashed password
        user = User(
            id=user_id,
            email=user_data.email,
            name=user_data.name,
            hashed_password=hashed_password  # Store the hashed password
        )

        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)

        log_user_action(user.id, "user_created", {"email": user.email})

        return UserRead(id=user.id, email=user.email, name=user.name)

    def authenticate_user(self, email: str, password: str) -> Optional[UserRead]:
        """Authenticate a user with email and password."""
        # Get user from database
        user = self.get_user_by_email(email)
        if not user:
            return None

        try:
            # Verify the password
            # The verify_password function handles the 72-byte bcrypt limitation
            if not verify_password(password, user.hashed_password):
                return None
        except Exception as e:
            # Handle password verification errors
            print(f"Password verification error: {str(e)}")
            return None

        log_user_action(user.id, "user_authenticated", {"email": email})
        return UserRead(id=user.id, email=user.email, name=user.name)

    def get_user_task_count(self, user_id: str) -> int:
        """Get the number of tasks for a user."""
        from sqlmodel import select
        statement = select(Task).where(Task.user_id == user_id)
        tasks = self.session.exec(statement).all()
        return len(tasks)

    def update_user(self, user_id: str, user_data: dict) -> Optional[UserRead]:
        """Update user information."""
        user = self.session.get(User, user_id)
        if not user:
            return None

        # Update user fields
        for field, value in user_data.items():
            if hasattr(user, field) and field != "id":
                setattr(user, field, value)

        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)

        log_user_action(user.id, "user_updated", {"updated_fields": list(user_data.keys())})
        return UserRead(id=user.id, email=user.email, name=user.name)

    def delete_user(self, user_id: str) -> bool:
        """Delete a user."""
        user = self.session.get(User, user_id)
        if not user:
            return False

        self.session.delete(user)
        self.session.commit()

        log_user_action(user.id, "user_deleted")
        return True