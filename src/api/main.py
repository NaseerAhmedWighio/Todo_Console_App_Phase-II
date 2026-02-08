from fastapi import FastAPI, HTTPException, Depends, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from typing import List
import logging

from src.models.task import TaskCreate, TaskUpdate, TaskResponse
from src.models.user import UserCreate, UserLogin, UserResponse, AuthToken
from src.storage.sqlite_storage import SQLiteStorage
from src.services.auth_service import AuthService
from src.utils.error_handlers import handle_error
from src.config import settings, get_allowed_origins

# Configure logging
logging.basicConfig(level=getattr(logging, settings.log_level.upper()))
logger = logging.getLogger(__name__)

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)
logger.info("Rate limiter initialized")

# Create the FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="REST API for the In-Memory Python Console App Todo Application",
)

# Add security middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_allowed_origins(),
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    max_age=3600,
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.allowed_origins.split(",") if settings.allowed_origins != "*" else ["*"]
)

# Add rate limiting middleware
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Initialize storage and service
storage = SQLiteStorage(settings.db_path)
auth_service = AuthService(storage)


def get_current_user(token: str = Header(None)) -> dict:
    """
    Dependency to get the current user from the token header.

    Args:
        token: Authorization token from header

    Returns:
        User information if token is valid

    Raises:
        HTTPException: If token is invalid or missing
    """
    if not token:
        raise HTTPException(status_code=401, detail="Authorization token required")

    if not auth_service.is_token_valid(token):
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = auth_service.get_user_from_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")

    return {"user_id": user.id, "username": user.username}


@app.get("/")
@limiter.limit("100/minute")
async def root(request: Request):
    """Root endpoint to verify the API is running."""
    return {"message": "Todo API is running", "version": settings.app_version}


# User authentication endpoints
@app.post("/auth/register", response_model=UserResponse, status_code=201)
@limiter.limit("10/minute")
async def register_user(request: Request, user_create: UserCreate):
    """
    Register a new user.
    """
    try:
        user = auth_service.create_user(user_create)
        if user is None:
            handle_error("Registration failed", 400, "Username or email already exists")

        logger.info(f"User registered successfully with ID: {user.id}")
        return user
    except Exception as e:
        logger.error(f"Error during registration: {str(e)}")
        handle_error("Failed to register user", 500)


@app.post("/auth/login", response_model=AuthToken)
@limiter.limit("20/minute")
async def login_user(request: Request, user_login: UserLogin):
    """
    Authenticate a user and return a token.
    """
    try:
        result = auth_service.authenticate_user(user_login)
        if result is None:
            handle_error("Login failed", 401, "Invalid username or password")

        logger.info(f"User logged in successfully: {result['username']}")
        return AuthToken(
            access_token=result["token"],
            token_type="bearer",
            user_id=result["user_id"],
            username=result["username"]
        )
    except Exception as e:
        logger.error(f"Error during login: {str(e)}")
        handle_error("Failed to login user", 500)


@app.post("/auth/logout", status_code=200)
@limiter.limit("20/minute")
async def logout_user(request: Request, token: str = Header(...)):
    """
    Logout the current user.
    """
    try:
        success = auth_service.logout_user(token)
        if success:
            logger.info("User logged out successfully")
            return {"message": "Logged out successfully"}
        else:
            handle_error("Logout failed", 400, "Invalid or expired token")
    except Exception as e:
        logger.error(f"Error during logout: {str(e)}")
        handle_error("Failed to logout user", 500)


@app.get("/tasks", response_model=List[TaskResponse])
@limiter.limit("50/minute")
async def get_all_tasks(request: Request, current_user: dict = Depends(get_current_user)):
    """
    Retrieve a list of all tasks for the current user.
    """
    try:
        tasks = auth_service.get_all_tasks(current_user["user_id"])
        logger.info(f"Retrieved {len(tasks)} tasks for user {current_user['user_id']}")
        return tasks
    except Exception as e:
        logger.error(f"Error retrieving tasks: {str(e)}")
        handle_error("Failed to retrieve tasks", 500)


@app.post("/tasks", response_model=TaskResponse, status_code=201)
@limiter.limit("20/minute")
async def create_task(request: Request, task_create: TaskCreate, current_user: dict = Depends(get_current_user)):
    """
    Add a new task to the system.
    """
    try:
        # Validate that description is not empty
        if not task_create.description or len(task_create.description.strip()) == 0:
            handle_error("Invalid input", 400, "Description must not be empty")

        task = auth_service.add_task(task_create, current_user["user_id"])
        if task is None:
            handle_error(
                "Failed to create task",
                500,
                "Task limit reached or other error occurred",
            )

        logger.info(f"Created task with ID: {task.id} for user {current_user['user_id']}")
        return task
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating task: {str(e)}")
        handle_error("Failed to create task", 500)


@app.get("/tasks/{task_id}", response_model=TaskResponse)
@limiter.limit("50/minute")
async def get_task(request: Request, task_id: str, current_user: dict = Depends(get_current_user)):
    """
    Retrieve a task by its ID.
    """
    try:
        task = auth_service.get_task(task_id, current_user["user_id"])
        if task is None:
            handle_error("Task not found", 404, f"Task with ID {task_id} not found")

        logger.info(f"Retrieved task with ID: {task_id}")
        return task
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving task {task_id}: {str(e)}")
        handle_error("Failed to retrieve task", 500)


@app.put("/tasks/{task_id}", response_model=TaskResponse)
@limiter.limit("20/minute")
async def update_task(request: Request, task_id: str, task_update: TaskUpdate, current_user: dict = Depends(get_current_user)):
    """
    Modify an existing task's description.
    """
    try:
        # Validate that description is not empty
        if not task_update.description or len(task_update.description.strip()) == 0:
            handle_error("Invalid input", 400, "Description must not be empty")

        updated_task = auth_service.update_task(task_id, task_update, current_user["user_id"])
        if updated_task is None:
            handle_error("Task not found", 404, f"Task with ID {task_id} not found")

        logger.info(f"Updated task with ID: {task_id}")
        return updated_task
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating task {task_id}: {str(e)}")
        handle_error("Failed to update task", 500)


@app.delete("/tasks/{task_id}", status_code=204)
@limiter.limit("20/minute")
async def delete_task(request: Request, task_id: str, current_user: dict = Depends(get_current_user)):
    """
    Remove a task from the system.
    """
    try:
        success = auth_service.delete_task(task_id, current_user["user_id"])
        if not success:
            handle_error("Task not found", 404, f"Task with ID {task_id} not found")

        logger.info(f"Deleted task with ID: {task_id}")
        return
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting task {task_id}: {str(e)}")
        handle_error("Failed to delete task", 500)


@app.put("/tasks/{task_id}/complete", response_model=TaskResponse)
@limiter.limit("20/minute")
async def mark_task_complete(request: Request, task_id: str, current_user: dict = Depends(get_current_user)):
    """
    Change a task's status to complete.
    """
    try:
        task = auth_service.mark_task_complete(task_id, current_user["user_id"])
        if task is None:
            handle_error("Task not found", 404, f"Task with ID {task_id} not found")

        logger.info(f"Marked task {task_id} as complete")
        return task
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error marking task {task_id} as complete: {str(e)}")
        handle_error("Failed to mark task as complete", 500)


@app.put("/tasks/{task_id}/incomplete", response_model=TaskResponse)
@limiter.limit("20/minute")
async def mark_task_incomplete(request: Request, task_id: str, current_user: dict = Depends(get_current_user)):
    """
    Change a task's status to incomplete.
    """
    try:
        task = auth_service.mark_task_incomplete(task_id, current_user["user_id"])
        if task is None:
            handle_error("Task not found", 404, f"Task with ID {task_id} not found")

        logger.info(f"Marked task {task_id} as incomplete")
        return task
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error marking task {task_id} as incomplete: {str(e)}")
        handle_error("Failed to mark task as incomplete", 500)


@app.get("/health")
@limiter.limit("100/minute")
async def health_check(request: Request):
    """Health check endpoint."""
    return {"status": "healthy", "task_count": 0, "user_authenticated": False}
