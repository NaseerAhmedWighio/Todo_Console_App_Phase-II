"""Authentication endpoints for Todo App backend."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import Annotated
from database.session import get_session
from models.user import User
from schemas.user import UserCreate, UserLogin, Token, UserRead
from services.user_service import UserService
from core.jwt import create_access_token
from core.config import settings
from datetime import timedelta
from core.logging import log_api_request, log_user_action
from api.deps import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead)
def register(user_data: UserCreate, session: Annotated[Session, Depends(get_session)]):
    """Register a new user - this should normally not be called directly as Better Auth handles registration."""
    # This endpoint exists for compatibility but in a real Better Auth setup,
    # registration would be handled by Better Auth on the frontend
    # The backend just validates JWT tokens from Better Auth
    user_service = UserService(session)

    try:
        print(f"Attempting to register user: {user_data.email}")
        print(f"Password length (raw): {len(user_data.password)} characters")
        print(f"Password length (bytes): {len(user_data.password.encode('utf-8'))} bytes")

        # Validate password length before attempting to create user
        # password_bytes = user_data.password.encode('utf-8')
        # if len(password_bytes) > 128:
        #     raise HTTPException(
        #         status_code=status.HTTP_400_BAD_REQUEST,
        #         detail="Password must be 128 bytes or less"
            # )
        # Pass the original password to the user service which will handle bcrypt hashing
        # The schema validation already handles password length requirements
        user = user_service.create_user(user_data)
        print(f"User created successfully: {user.id}")
        log_user_action(user.id, "registration_success", {"email": user.email})
        log_api_request("/auth/register", "POST", user.id)
        return user
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        print(f"Registration failed with error: {str(e)}")
        print(f"Error type: {type(e)}")
        import traceback
        traceback.print_exc()  # Print full stack trace
        log_user_action(None, "registration_failed", {"error": str(e)})

        # Provide user-friendly error message
        error_detail = str(e)
        print(f"Raw error detail: {error_detail}")

        if "72 bytes" in error_detail or "password" in error_detail.lower() or "Password too long" in error_detail or "could not be processed" in error_detail:
            error_detail = "Password could not be processed. Please try a simple password like 'mypassword123'."
        elif "duplicate" in error_detail.lower() or "unique" in error_detail.lower():
            error_detail = "Email already exists. Please use a different email."
        elif "Password validation failed" in error_detail:
            error_detail = "Invalid password. Please try a different password."
        else:
            # For other errors, provide more generic message but log the original
            error_detail = f"Registration failed: {type(e).__name__}. Please try again."

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_detail
        )


@router.post("/login", response_model=Token)
def login(form_data: UserLogin, session: Annotated[Session, Depends(get_session)]):
    """Login endpoint - this should normally not be called directly as Better Auth handles authentication."""
    # This endpoint exists for compatibility but in a real Better Auth setup,
    # authentication would be handled by Better Auth on the frontend
    # The backend just validates JWT tokens from Better Auth
    user_service = UserService(session)

    try:
        print(f"Attempting to login user: {form_data.email}")
        print(f"Password length (raw): {len(form_data.password)} characters")
        print(f"Password length (bytes): {len(form_data.password.encode('utf-8'))} bytes")


        user = user_service.authenticate_user(form_data.email, form_data.password)
        if not user:
            log_user_action(None, "login_failed", {"email": form_data.email})
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Handle other exceptions
        print(f"Login failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        log_user_action(None, "login_failed", {"email": form_data.email, "error": str(e)})
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Login failed: {str(e)}"
        )

    # Create access token
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.id}, expires_delta=access_token_expires
    )

    log_user_action(user.id, "login_success", {"email": user.email})
    log_api_request("/auth/login", "POST", user.id)

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/logout")
def logout():
    """Logout user (handled by frontend clearing tokens)."""
    # In a real implementation, this would be handled by Better Auth
    # For now, just return success
    return {"message": "Successfully logged out"}


@router.get("/me", response_model=UserRead)
def get_current_user_endpoint(current_user: User = Depends(get_current_user)):
    """Get current user information (requires valid JWT token)."""
    # Return user information based on the token
    return current_user