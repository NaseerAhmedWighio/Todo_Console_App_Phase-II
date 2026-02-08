"""Task endpoints for Todo App backend."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import Annotated, List, Optional
from database.session import get_session
from api.deps import get_current_user
from models.user import User
from schemas.task import TaskRead, TaskCreate, TaskUpdate, TaskComplete
from services.task_service import TaskService
from schemas.task import TaskListResponse
from core.logging import log_api_request

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/{user_id}/tasks", response_model=List[TaskRead])
def get_tasks(
    user_id: str,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[Session, Depends(get_session)],
    completed: Optional[bool] = None,
    search: Optional[str] = None,
):
    """Get all tasks for the specified user with optional filtering."""
    # Verify the user is accessing their own tasks (user data isolation)
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only access your own tasks"
        )

    task_service = TaskService(session)
    tasks = task_service.get_tasks_for_user(user_id, completed=completed, search=search)

    log_api_request(f"/api/{user_id}/tasks", "GET", current_user.id)
    return tasks


@router.post("/{user_id}/tasks", response_model=TaskRead)
def create_task(
    user_id: str,
    task_data: TaskCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[Session, Depends(get_session)]
):
    """Create a new task for the specified user."""
    # Verify the user is creating tasks for themselves
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only create tasks for yourself"
        )

    task_service = TaskService(session)
    task = task_service.create_task(task_data, user_id)

    log_api_request(f"/api/{user_id}/tasks", "POST", current_user.id)
    return task


@router.get("/{user_id}/tasks/{task_id}", response_model=TaskRead)
def get_task(
    user_id: str,
    task_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[Session, Depends(get_session)]
):
    """Get a specific task for the specified user."""
    # Verify the user is accessing their own task
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only access your own tasks"
        )

    task_service = TaskService(session)
    task = task_service.get_task_by_id(task_id, user_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    log_api_request(f"/api/{user_id}/tasks/{task_id}", "GET", current_user.id)
    return task


@router.put("/{user_id}/tasks/{task_id}", response_model=TaskRead)
def update_task(
    user_id: str,
    task_id: int,
    task_data: TaskUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[Session, Depends(get_session)]
):
    """Update a specific task for the specified user."""
    # Verify the user is updating their own task
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own tasks"
        )

    task_service = TaskService(session)
    task = task_service.update_task(task_id, task_data, user_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    log_api_request(f"/api/{user_id}/tasks/{task_id}", "PUT", current_user.id)
    return task


@router.delete("/{user_id}/tasks/{task_id}")
def delete_task(
    user_id: str,
    task_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[Session, Depends(get_session)]
):
    """Delete a specific task for the specified user."""
    # Verify the user is deleting their own task
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own tasks"
        )

    task_service = TaskService(session)
    success = task_service.delete_task(task_id, user_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    log_api_request(f"/api/{user_id}/tasks/{task_id}", "DELETE", current_user.id)
    return {"message": "Task deleted successfully"}


@router.patch("/{user_id}/tasks/{task_id}/complete", response_model=TaskRead)
def toggle_task_completion(
    user_id: str,
    task_id: int,
    completion_data: TaskComplete,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[Session, Depends(get_session)]
):
    """Toggle the completion status of a specific task for the specified user."""
    # Verify the user is updating their own task
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own tasks"
        )

    task_service = TaskService(session)
    task = task_service.toggle_task_completion(task_id, completion_data, user_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    log_api_request(f"/api/{user_id}/tasks/{task_id}/complete", "PATCH", current_user.id)
    return task