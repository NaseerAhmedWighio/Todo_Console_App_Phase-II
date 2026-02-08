"""Task service for Todo App backend."""
from sqlmodel import Session, select, func
from typing import List, Optional
from models.task import Task
from schemas.task import TaskCreate, TaskUpdate, TaskComplete
from core.logging import log_user_action
from fastapi import HTTPException, status
from sqlalchemy import or_


class TaskService:
    """Service class for task-related operations."""

    def __init__(self, session: Session):
        """Initialize with database session."""
        self.session = session

    def get_tasks_for_user(self, user_id: str, completed: Optional[bool] = None, search: Optional[str] = None) -> List[Task]:
        """Get all tasks for a specific user with optional filtering."""
        statement = select(Task).where(Task.user_id == user_id)

        # Apply completion filter if specified
        if completed is not None:
            statement = statement.where(Task.completed == completed)

        # Apply search filter if specified
        if search:
            statement = statement.where(or_(Task.title.contains(search), Task.description.contains(search)))

        tasks = self.session.exec(statement).all()

        log_user_action(user_id, "tasks_fetched", {"count": len(tasks), "filters": {"completed": completed, "search": search}})
        return tasks

    def get_task_by_id(self, task_id: int, user_id: str) -> Optional[Task]:
        """Get a specific task by ID for a user."""
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        task = self.session.exec(statement).first()

        if task:
            log_user_action(user_id, "task_fetched", {"task_id": task_id})
        else:
            log_user_action(user_id, "task_fetch_failed", {"task_id": task_id, "reason": "not_found"})

        return task

    def create_task(self, task_data: TaskCreate, user_id: str) -> Task:
        """Create a new task for a user."""
        task = Task(
            title=task_data.title,
            description=task_data.description,
            completed=task_data.completed,
            user_id=user_id
        )

        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)

        log_user_action(user_id, "task_created", {"task_id": task.id, "title": task.title})
        return task

    def update_task(self, task_id: int, task_data: TaskUpdate, user_id: str) -> Optional[Task]:
        """Update an existing task for a user."""
        from datetime import datetime

        task = self.get_task_by_id(task_id, user_id)
        if not task:
            return None

        # Update task fields
        update_data = task_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            if hasattr(task, field):
                setattr(task, field, value)

        task.updated_at = datetime.utcnow()
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)

        log_user_action(user_id, "task_updated", {"task_id": task_id})
        return task

    def delete_task(self, task_id: int, user_id: str) -> bool:
        """Delete a task for a user."""
        task = self.get_task_by_id(task_id, user_id)
        if not task:
            return False

        self.session.delete(task)
        self.session.commit()

        log_user_action(user_id, "task_deleted", {"task_id": task_id})
        return True

    def toggle_task_completion(self, task_id: int, completion_status: TaskComplete, user_id: str) -> Optional[Task]:
        """Toggle the completion status of a task."""
        task = self.get_task_by_id(task_id, user_id)
        if not task:
            return None

        task.completed = completion_status.completed
        from datetime import datetime
        task.updated_at = datetime.utcnow()
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)

        log_user_action(user_id, "task_completion_toggled", {
            "task_id": task_id,
            "completed": completion_status.completed
        })
        return task