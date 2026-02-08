from typing import List, Optional
from src.storage.in_memory import InMemoryStorage
from src.models.task import Task, TaskCreate, TaskUpdate
from src.models.user import User, UserCreate, UserLogin, hash_password
import logging


class CLITodoService:
    """
    Service layer that implements the business logic for todo operations
    with atomic operations to prevent race conditions as required by the constitution.
    This service manages user sessions for CLI applications.
    """

    def __init__(self, storage: InMemoryStorage):
        self.storage = storage
        self.logger = logging.getLogger(__name__)
        self.current_user_id = None  # Track the currently authenticated user

    def set_current_user(self, user_id: str):
        """Set the current user ID for the session."""
        self.current_user_id = user_id

    def clear_current_user(self):
        """Clear the current user ID."""
        self.current_user_id = None

    def register_user(self, user_create: UserCreate) -> Optional[User]:
        """
        Register a new user with the provided details.

        Args:
            user_create: Object containing the user registration details

        Returns:
            The created User object if successful, None otherwise
        """
        try:
            # Hash the password
            password_hash = hash_password(user_create.password)

            # Create a new user with the provided details
            new_user = User(
                username=user_create.username,
                email=user_create.email,
                password_hash=password_hash,
            )

            # Attempt to create the user in storage
            success = self.storage.create_user(new_user)

            if success:
                self.logger.info(f"Successfully registered user with ID: {new_user.id}")
                return new_user
            else:
                self.logger.error(
                    "Failed to register user - possibly duplicate username or email"
                )
                return None

        except Exception as e:
            self.logger.error(f"Error registering user: {str(e)}")
            return None

    def login_user(self, user_login: UserLogin) -> Optional[dict]:
        """
        Authenticate a user with the provided credentials.

        Args:
            user_login: Object containing the username and password

        Returns:
            A dictionary with user info and token if successful, None otherwise
        """
        try:
            # Attempt to authenticate the user
            user = self.storage.authenticate_user(user_login.username, user_login.password)

            if user:
                self.logger.info(f"Successfully logged in user: {user.username}")
                # Set current user for this session
                self.set_current_user(user.id)

                # Return user info and token
                return {
                    "user_id": user.id,
                    "username": user.username,
                    "token": f"fake-jwt-{user.id}"  # In a real app, use proper JWT
                }
            else:
                self.logger.warning(f"Failed login attempt for username: {user_login.username}")
                return None

        except Exception as e:
            self.logger.error(f"Error during login: {str(e)}")
            return None

    def logout_user(self) -> bool:
        """
        Logout the current user.

        Returns:
            True if logout was successful, False otherwise
        """
        try:
            if self.current_user_id:
                self.logger.info(f"User {self.current_user_id} logged out")
                self.clear_current_user()
                return True
            else:
                return False
        except Exception as e:
            self.logger.error(f"Error during logout: {str(e)}")
            return False

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
            if not self.current_user_id:
                self.logger.error("User must be authenticated to add a task")
                return None

            # Create a new task with the provided description and default values
            new_task = Task(
                description=task_create.description,
                status="incomplete",  # Default to incomplete as per requirements
            )

            # Attempt to add the task to storage with user_id
            success = self.storage.add_task(new_task, self.current_user_id)

            if success:
                self.logger.info(f"Successfully added task with ID: {new_task.id} for user: {self.current_user_id}")
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
            if not self.current_user_id:
                self.logger.error("User must be authenticated to retrieve a task")
                return None

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
        Retrieve all tasks for the current user.

        Returns:
            A list of all Task objects for the current user
        """
        try:
            if not self.current_user_id:
                self.logger.error("User must be authenticated to retrieve tasks")
                return []

            tasks = self.storage.get_tasks_by_user(self.current_user_id)
            self.logger.info(f"Retrieved {len(tasks)} tasks for user: {self.current_user_id}")
            return tasks
        except Exception as e:
            self.logger.error(f"Error retrieving tasks for user {self.current_user_id}: {str(e)}")
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
            if not self.current_user_id:
                self.logger.error("User must be authenticated to update a task")
                return None

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
            if not self.current_user_id:
                self.logger.error("User must be authenticated to delete a task")
                return False

            success = self.storage.delete_task(task_id, self.current_user_id)
            if success:
                self.logger.info(f"Successfully deleted task with ID: {task_id}")
            else:
                self.logger.warning(
                    f"Failed to delete task - task with ID {task_id} not found or not owned by user"
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
            if not self.current_user_id:
                self.logger.error("User must be authenticated to mark a task complete")
                return None

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
            if not self.current_user_id:
                self.logger.error("User must be authenticated to mark a task incomplete")
                return None

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
        Get the current number of tasks for the current user.

        Returns:
            The number of tasks for the current user
        """
        try:
            if not self.current_user_id:
                self.logger.error("User must be authenticated to get task count")
                return 0

            # Get tasks for the current user
            tasks = self.storage.get_tasks_by_user(self.current_user_id)
            count = len(tasks)
            self.logger.info(f"Current task count for user {self.current_user_id}: {count}")
            return count
        except Exception as e:
            self.logger.error(f"Error getting task count: {str(e)}")
            return 0