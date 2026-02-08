import threading
from typing import Dict, List, Optional
from src.models.task import Task
from src.models.user import User
from src.db.task_db import TaskDB
import time


class SQLiteStorage:
    """
    SQLite storage implementation that provides thread-safe operations
    to store tasks in SQLite database with persistent storage as required by the constitution.
    """

    def __init__(self, db_path: str = "todo_app.db"):
        self.db = TaskDB(db_path)
        self._lock = threading.RLock()  # Reentrant lock for thread safety
        self._perf_stats = {
            'get_task_calls': 0,
            'get_task_time': 0.0,
            'add_task_calls': 0,
            'add_task_time': 0.0,
            'update_task_calls': 0,
            'update_task_time': 0.0,
            'delete_task_calls': 0,
            'delete_task_time': 0.0,
        }

    def add_task(self, task: Task, user_id: str = None) -> bool:
        """
        Add a task to the SQLite database.

        Args:
            task: The task to add
            user_id: The ID of the user adding the task

        Returns:
            True if the task was added successfully, False otherwise
        """
        start_time = time.time()
        try:
            with self._lock:
                if user_id:
                    return self.db.add_task(task, user_id)
                else:
                    return self.db.add_task(task, "anonymous")  # Fallback for backward compatibility
        finally:
            elapsed = time.time() - start_time
            self._perf_stats['add_task_calls'] += 1
            self._perf_stats['add_task_time'] += elapsed

    def get_task(self, task_id: str) -> Optional[Task]:
        """
        Retrieve a task by its ID from the database.

        Args:
            task_id: The ID of the task to retrieve

        Returns:
            The task if found, None otherwise
        """
        start_time = time.time()
        try:
            with self._lock:
                return self.db.get_task(task_id)
        finally:
            elapsed = time.time() - start_time
            self._perf_stats['get_task_calls'] += 1
            self._perf_stats['get_task_time'] += elapsed

    def get_tasks_by_user(self, user_id: str) -> List[Task]:
        """
        Retrieve all tasks for a specific user from the database.

        Args:
            user_id: The ID of the user whose tasks to retrieve

        Returns:
            A list of tasks belonging to the user
        """
        with self._lock:
            return self.db.get_tasks_by_user(user_id)

    def get_all_tasks(self) -> List[Task]:
        """
        Retrieve all tasks from the database.

        Returns:
            A list of all tasks
        """
        with self._lock:
            return self.db.get_all_tasks()

    def update_task(self, task_id: str, updated_task: Task) -> bool:
        """
        Update an existing task in the database.

        Args:
            task_id: The ID of the task to update
            updated_task: The updated task object

        Returns:
            True if the task was updated successfully, False otherwise
        """
        start_time = time.time()
        try:
            with self._lock:
                return self.db.update_task(task_id, updated_task)
        finally:
            elapsed = time.time() - start_time
            self._perf_stats['update_task_calls'] += 1
            self._perf_stats['update_task_time'] += elapsed

    def delete_task(self, task_id: str, user_id: str = None) -> bool:
        """
        Delete a task by its ID from the database.

        Args:
            task_id: The ID of the task to delete
            user_id: The ID of the user requesting deletion (to verify ownership)

        Returns:
            True if the task was deleted successfully, False otherwise
        """
        start_time = time.time()
        try:
            with self._lock:
                return self.db.delete_task(task_id, user_id)
        finally:
            elapsed = time.time() - start_time
            self._perf_stats['delete_task_calls'] += 1
            self._perf_stats['delete_task_time'] += elapsed

    def clear_all(self):
        """
        Clear all tasks from the database (used for testing/resetting).
        """
        with self._lock:
            self.db.clear_all_tasks()

    def get_task_count(self) -> int:
        """
        Get the current number of tasks in storage.

        Returns:
            The number of tasks in storage
        """
        with self._lock:
            return self.db.get_task_count()

    # User-related methods
    def create_user(self, user: User) -> bool:
        """
        Create a new user in the database.

        Args:
            user: The user to create

        Returns:
            True if the user was created successfully, False otherwise
        """
        with self._lock:
            return self.db.create_user(user)

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """
        Retrieve a user by their ID from the database.

        Args:
            user_id: The ID of the user to retrieve

        Returns:
            The user if found, None otherwise
        """
        with self._lock:
            return self.db.get_user_by_id(user_id)

    def get_user_by_username(self, username: str) -> Optional[User]:
        """
        Retrieve a user by their username from the database.

        Args:
            username: The username of the user to retrieve

        Returns:
            The user if found, None otherwise
        """
        with self._lock:
            return self.db.get_user_by_username(username)

    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Retrieve a user by their email from the database.

        Args:
            email: The email of the user to retrieve

        Returns:
            The user if found, None otherwise
        """
        with self._lock:
            return self.db.get_user_by_email(email)

    def update_user(self, user_id: str, username: str = None, email: str = None, password_hash: str = None) -> bool:
        """
        Update a user's information in the database.

        Args:
            user_id: The ID of the user to update
            username: New username (optional)
            email: New email (optional)
            password_hash: New password hash (optional)

        Returns:
            True if the user was updated successfully, False otherwise
        """
        with self._lock:
            return self.db.update_user(user_id, username, email, password_hash)

    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """
        Authenticate a user by username and password.

        Args:
            username: The username to authenticate
            password: The plain text password to verify

        Returns:
            The user object if authentication succeeds, None otherwise
        """
        with self._lock:
            return self.db.authenticate_user(username, password)

    def delete_user(self, user_id: str) -> bool:
        """
        Delete a user and all their tasks from the database.

        Args:
            user_id: The ID of the user to delete

        Returns:
            True if the user was deleted successfully, False otherwise
        """
        with self._lock:
            return self.db.delete_user(user_id)

    def get_performance_stats(self) -> dict:
        """
        Get performance statistics for the storage operations.

        Returns:
            Dictionary containing performance statistics
        """
        with self._lock:
            stats = self._perf_stats.copy()
            # Calculate average times
            if stats['get_task_calls'] > 0:
                stats['avg_get_time'] = stats['get_task_time'] / stats['get_task_calls']
            else:
                stats['avg_get_time'] = 0.0

            if stats['add_task_calls'] > 0:
                stats['avg_add_time'] = stats['add_task_time'] / stats['add_task_calls']
            else:
                stats['avg_add_time'] = 0.0

            if stats['update_task_calls'] > 0:
                stats['avg_update_time'] = stats['update_task_time'] / stats['update_task_calls']
            else:
                stats['avg_update_time'] = 0.0

            if stats['delete_task_calls'] > 0:
                stats['avg_delete_time'] = stats['delete_task_time'] / stats['delete_task_calls']
            else:
                stats['avg_delete_time'] = 0.0

            return stats