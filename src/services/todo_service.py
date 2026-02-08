from typing import List, Optional
from src.storage.in_memory import InMemoryStorage
from src.models.task import Task, TaskCreate, TaskUpdate
import logging


class TodoService:
    """
    Service layer that implements the business logic for todo operations
    with atomic operations to prevent race conditions as required by the constitution.
    """

    def __init__(self, storage: InMemoryStorage):
        self.storage = storage
        self.logger = logging.getLogger(__name__)

    def add_task(self, task_create: TaskCreate) -> Optional[Task]:
        """
        Create a new task with the provided description and add it to the list
        with "incomplete" status as required by the constitution.

        Args:
            task_create: Object containing the task description

        Returns:
            The created Task object if successful, None otherwise
        """
        try:
            # Create a new task with the provided description and default values
            new_task = Task(
                description=task_create.description,
                status="incomplete",  # Default to incomplete as per requirements
            )

            # Attempt to add the task to storage
            success = self.storage.add_task(new_task)

            if success:
                self.logger.info(f"Successfully added task with ID: {new_task.id}")
                return new_task
            else:
                self.logger.error(
                    "Failed to add task - possibly exceeded max limit or ID conflict"
                )
                return None

        except Exception as e:
            self.logger.error(f"Error adding task: {str(e)}")
            return None

    def get_task(self, task_id: str) -> Optional[Task]:
        """
        Retrieve a specific task by its ID.

        Args:
            task_id: The ID of the task to retrieve

        Returns:
            The Task object if found, None otherwise
        """
        try:
            task = self.storage.get_task(task_id)
            if task:
                self.logger.info(f"Retrieved task with ID: {task_id}")
            else:
                self.logger.warning(f"Task with ID {task_id} not found")
            return task
        except Exception as e:
            self.logger.error(f"Error retrieving task with ID {task_id}: {str(e)}")
            return None

    def get_all_tasks(self) -> List[Task]:
        """
        Retrieve all tasks in the system.

        Returns:
            A list of all Task objects
        """
        try:
            tasks = self.storage.get_all_tasks()
            self.logger.info(f"Retrieved {len(tasks)} tasks")
            return tasks
        except Exception as e:
            self.logger.error(f"Error retrieving all tasks: {str(e)}")
            return []

    def update_task(self, task_id: str, task_update: TaskUpdate) -> Optional[Task]:
        """
        Modify the description of an existing task.

        Args:
            task_id: The ID of the task to update
            task_update: Object containing the new description

        Returns:
            The updated Task object if successful, None otherwise
        """
        try:
            # Get the existing task
            existing_task = self.storage.get_task(task_id)
            if not existing_task:
                self.logger.warning(
                    f"Cannot update task - task with ID {task_id} not found"
                )
                return None

            # Create an updated task with new description but preserve other fields
            updated_task = Task(
                id=existing_task.id,
                description=task_update.description,
                status=existing_task.status,  # Preserve the current status
                created_date=existing_task.created_date,  # Preserve the creation date
            )

            # Update the task in storage
            success = self.storage.update_task(task_id, updated_task)

            if success:
                self.logger.info(f"Successfully updated task with ID: {task_id}")
                return updated_task
            else:
                self.logger.error(f"Failed to update task with ID: {task_id}")
                return None

        except Exception as e:
            self.logger.error(f"Error updating task with ID {task_id}: {str(e)}")
            return None

    def delete_task(self, task_id: str) -> bool:
        """
        Remove a task from the list by its ID.

        Args:
            task_id: The ID of the task to delete

        Returns:
            True if the task was deleted successfully, False otherwise
        """
        try:
            success = self.storage.delete_task(task_id)
            if success:
                self.logger.info(f"Successfully deleted task with ID: {task_id}")
            else:
                self.logger.warning(
                    f"Failed to delete task - task with ID {task_id} not found"
                )
            return success
        except Exception as e:
            self.logger.error(f"Error deleting task with ID {task_id}: {str(e)}")
            return False

    def mark_task_complete(self, task_id: str) -> Optional[Task]:
        """
        Change a task's status to "complete".

        Args:
            task_id: The ID of the task to mark as complete

        Returns:
            The updated Task object if successful, None otherwise
        """
        try:
            # Get the existing task
            existing_task = self.storage.get_task(task_id)
            if not existing_task:
                self.logger.warning(
                    f"Cannot mark task complete - task with ID {task_id} not found"
                )
                return None

            # Create an updated task with new status but preserve other fields
            updated_task = Task(
                id=existing_task.id,
                description=existing_task.description,
                status="complete",
                created_date=existing_task.created_date,
            )

            # Update the task in storage
            success = self.storage.update_task(task_id, updated_task)

            if success:
                self.logger.info(f"Successfully marked task {task_id} as complete")
                return updated_task
            else:
                self.logger.error(f"Failed to mark task {task_id} as complete")
                return None

        except Exception as e:
            self.logger.error(f"Error marking task {task_id} as complete: {str(e)}")
            return None

    def mark_task_incomplete(self, task_id: str) -> Optional[Task]:
        """
        Change a task's status to "incomplete".

        Args:
            task_id: The ID of the task to mark as incomplete

        Returns:
            The updated Task object if successful, None otherwise
        """
        try:
            # Get the existing task
            existing_task = self.storage.get_task(task_id)
            if not existing_task:
                self.logger.warning(
                    f"Cannot mark task incomplete - task with ID {task_id} not found"
                )
                return None

            # Create an updated task with new status but preserve other fields
            updated_task = Task(
                id=existing_task.id,
                description=existing_task.description,
                status="incomplete",
                created_date=existing_task.created_date,
            )

            # Update the task in storage
            success = self.storage.update_task(task_id, updated_task)

            if success:
                self.logger.info(f"Successfully marked task {task_id} as incomplete")
                return updated_task
            else:
                self.logger.error(f"Failed to mark task {task_id} as incomplete")
                return None

        except Exception as e:
            self.logger.error(f"Error marking task {task_id} as incomplete: {str(e)}")
            return None

    def get_task_count(self) -> int:
        """
        Get the current number of tasks in the system.

        Returns:
            The number of tasks in the system
        """
        try:
            count = self.storage.get_task_count()
            self.logger.info(f"Current task count: {count}")
            return count
        except Exception as e:
            self.logger.error(f"Error getting task count: {str(e)}")
            return 0