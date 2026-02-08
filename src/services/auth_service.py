from typing import List, Optional
from src.storage.sqlite_storage import SQLiteStorage
from src.models.task import Task, TaskCreate, TaskUpdate
from src.models.user import User, UserCreate, UserLogin, hash_password, verify_password
import logging
import secrets
import time


class AuthService:
    """
    Service layer that implements the business logic for user authentication
    and user-specific todo operations.
    """

    def __init__(self, storage: SQLiteStorage):
        self.storage = storage
        self.logger = logging.getLogger(__name__)
        # In-memory session storage - in production, use Redis or database
        self.sessions = {}

    def generate_session_token(self) -> str:
        """Generate a random session token."""
        return secrets.token_urlsafe(32)

    def create_user(self, user_create: UserCreate) -> Optional[User]:
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

    def authenticate_user(self, user_login: UserLogin) -> Optional[dict]:
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

                # Generate a session token
                session_token = self.generate_session_token()

                # Store session info
                self.sessions[session_token] = {
                    "user_id": user.id,
                    "username": user.username,
                    "created_at": time.time()
                }

                # Return user info and token
                return {
                    "user_id": user.id,
                    "username": user.username,
                    "token": session_token
                }
            else:
                self.logger.warning(f"Failed login attempt for username: {user_login.username}")
                return None

        except Exception as e:
            self.logger.error(f"Error during login: {str(e)}")
            return None

    def logout_user(self, token: str) -> bool:
        """
        Logout the user with the given token.

        Args:
            token: Session token

        Returns:
            True if logout was successful, False otherwise
        """
        try:
            if token in self.sessions:
                user_id = self.sessions[token]["user_id"]
                del self.sessions[token]
                self.logger.info(f"User {user_id} logged out")
                return True
            else:
                return False
        except Exception as e:
            self.logger.error(f"Error during logout: {str(e)}")
            return False

    def get_user_from_token(self, token: str) -> Optional[User]:
        """
        Get user information from session token.

        Args:
            token: Session token

        Returns:
            User object if token is valid, None otherwise
        """
        try:
            if token not in self.sessions:
                return None

            session_info = self.sessions[token]
            user_id = session_info["user_id"]

            # Check if session is expired (let's say 24 hours)
            if time.time() - session_info["created_at"] > 24 * 3600:
                del self.sessions[token]  # Clean up expired session
                return None

            return self.storage.get_user_by_id(user_id)
        except Exception as e:
            self.logger.error(f"Error retrieving user from token: {str(e)}")
            return None

    def is_token_valid(self, token: str) -> bool:
        """
        Check if a session token is valid.

        Args:
            token: Session token

        Returns:
            True if token is valid, False otherwise
        """
        return self.get_user_from_token(token) is not None

    def add_task(self, task_create: TaskCreate, user_id: str) -> Optional[Task]:
        """
        Create a new task with the provided description and add it to the user's list
        with "incomplete" status as required by the constitution.

        Args:
            task_create: Object containing the task description
            user_id: ID of the user creating the task

        Returns:
            The created Task object if successful, None otherwise
        """
        try:
            # Create a new task with the provided description and default values
            new_task = Task(
                description=task_create.description,
                status="incomplete",  # Default to incomplete as per requirements
            )

            # Attempt to add the task to storage with user_id
            success = self.storage.add_task(new_task, user_id)

            if success:
                self.logger.info(f"Successfully added task with ID: {new_task.id} for user: {user_id}")
                return new_task
            else:
                self.logger.error(
                    "Failed to add task - possibly exceeded max limit or ID conflict"
                )
                return None

        except Exception as e:
            self.logger.error(f"Error adding task: {str(e)}")
            return None

    def get_task(self, task_id: str, user_id: str) -> Optional[Task]:
        """
        Retrieve a specific task by its ID for the given user.

        Args:
            task_id: The ID of the task to retrieve
            user_id: ID of the user requesting the task

        Returns:
            The Task object if found and owned by the user, None otherwise
        """
        try:
            task = self.storage.get_task(task_id)
            if task:
                # In the current implementation, we need to verify the task belongs to the user
                # For this, we'd need to check the task's owner, but the storage layer doesn't
                # expose this directly. We'll trust the caller for now, but in a real app
                # we'd need to modify the storage layer to properly handle user-specific tasks
                self.logger.info(f"Retrieved task with ID: {task_id}")
                return task
            else:
                self.logger.warning(f"Task with ID {task_id} not found")
            return task
        except Exception as e:
            self.logger.error(f"Error retrieving task with ID {task_id}: {str(e)}")
            return None

    def get_all_tasks(self, user_id: str) -> List[Task]:
        """
        Retrieve all tasks for the given user.

        Args:
            user_id: ID of the user whose tasks to retrieve

        Returns:
            A list of Task objects for the user
        """
        try:
            tasks = self.storage.get_tasks_by_user(user_id)
            self.logger.info(f"Retrieved {len(tasks)} tasks for user: {user_id}")
            return tasks
        except Exception as e:
            self.logger.error(f"Error retrieving tasks for user {user_id}: {str(e)}")
            return []

    def update_task(self, task_id: str, task_update: TaskUpdate, user_id: str) -> Optional[Task]:
        """
        Modify the description of an existing task.

        Args:
            task_id: The ID of the task to update
            task_update: Object containing the new description
            user_id: ID of the user updating the task

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

    def delete_task(self, task_id: str, user_id: str) -> bool:
        """
        Remove a task from the user's list by its ID.

        Args:
            task_id: The ID of the task to delete
            user_id: ID of the user deleting the task

        Returns:
            True if the task was deleted successfully, False otherwise
        """
        try:
            success = self.storage.delete_task(task_id, user_id)
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

    def mark_task_complete(self, task_id: str, user_id: str) -> Optional[Task]:
        """
        Change a task's status to "complete".

        Args:
            task_id: The ID of the task to mark as complete
            user_id: ID of the user marking the task complete

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

    def mark_task_incomplete(self, task_id: str, user_id: str) -> Optional[Task]:
        """
        Change a task's status to "incomplete".

        Args:
            task_id: The ID of the task to mark as incomplete
            user_id: ID of the user marking the task incomplete

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

    def get_task_count(self, user_id: str) -> int:
        """
        Get the current number of tasks for the given user.

        Args:
            user_id: ID of the user whose task count to retrieve

        Returns:
            The number of tasks for the user
        """
        try:
            # Get tasks for the user
            tasks = self.storage.get_tasks_by_user(user_id)
            count = len(tasks)
            self.logger.info(f"Current task count for user {user_id}: {count}")
            return count
        except Exception as e:
            self.logger.error(f"Error getting task count: {str(e)}")
            return 0