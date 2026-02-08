from fastapi import HTTPException, status
from typing import Optional
import logging


class TodoAppError(Exception):
    """Base exception class for the todo application"""

    pass


class TaskNotFoundError(TodoAppError):
    """Raised when a task is not found"""

    pass


class TaskValidationError(TodoAppError):
    """Raised when task validation fails"""

    pass


class TaskLimitReachedError(TodoAppError):
    """Raised when the maximum number of tasks is reached"""

    pass


def handle_error(
    error_msg: str,
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail: Optional[str] = None,
):
    """
    Generic error handler that raises HTTPException with proper status codes.

    Args:
        error_msg: The main error message
        status_code: The HTTP status code to return
        detail: Additional details about the error
    """
    logging.error(f"{error_msg}. Detail: {detail}")
    raise HTTPException(status_code=status_code, detail=detail or error_msg)


def validate_task_exists(task, task_id: str):
    """
    Validates that a task exists and raises appropriate error if not.

    Args:
        task: The task object to check (None if not found)
        task_id: The ID of the task being checked

    Raises:
        TaskNotFoundError if the task does not exist
    """
    if task is None:
        raise TaskNotFoundError(f"Task with ID {task_id} not found")
