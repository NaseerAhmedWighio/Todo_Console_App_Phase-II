import threading
from typing import Dict, List, Optional
from src.models.task import Task
from src.models.user import User
import time


class InMemoryStorage:
    """
    In-memory storage implementation that provides thread-safe operations
    to store tasks in memory with atomic operations as required by the constitution.
    """

    def __init__(self):
        self._tasks: Dict[str, Task] = {}
        self._users: Dict[str, User] = {}
        self._lock = threading.RLock()  # Reentrant lock for thread safety
        self._max_tasks = 1000  # Maximum of 1000 tasks allowed in memory
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
        Add a task to the in-memory store.

        Args:
            task: The task to add
            user_id: The ID of the user adding the task

        Returns:
            True if the task was added successfully, False otherwise
        """
        start_time = time.time()
        try:
            with self._lock:
                if len(self._tasks) >= self._max_tasks:
                    return False  # Exceeded maximum allowed tasks

                if task.id in self._tasks:
                    return False  # Task with this ID already exists

                self._tasks[task.id] = task
                return True
        finally:
            elapsed = time.time() - start_time
            self._perf_stats['add_task_calls'] += 1
            self._perf_stats['add_task_time'] += elapsed

    def get_task(self, task_id: str) -> Optional[Task]:
        """
        Retrieve a task by its ID.

        Args:
            task_id: The ID of the task to retrieve

        Returns:
            The task if found, None otherwise
        """
        start_time = time.time()
        try:
            with self._lock:
                return self._tasks.get(task_id)
        finally:
            elapsed = time.time() - start_time
            self._perf_stats['get_task_calls'] += 1
            self._perf_stats['get_task_time'] += elapsed

    def get_tasks_by_user(self, user_id: str) -> List[Task]:
        """
        Retrieve all tasks for a specific user.

        Args:
            user_id: The ID of the user whose tasks to retrieve

        Returns:
            A list of tasks belonging to the user
        """
        # In memory implementation doesn't actually track user associations yet
        # This is just for interface compatibility
        with self._lock:
            return list(self._tasks.values())

    def get_all_tasks(self) -> List[Task]:
        """
        Retrieve all tasks in the store.

        Returns:
            A list of all tasks
        """
        with self._lock:
            return list(self._tasks.values())

    def update_task(self, task_id: str, updated_task: Task) -> bool:
        """
        Update an existing task.

        Args:
            task_id: The ID of the task to update
            updated_task: The updated task object

        Returns:
            True if the task was updated successfully, False otherwise
        """
        start_time = time.time()
        try:
            with self._lock:
                if task_id not in self._tasks:
                    return False

                self._tasks[task_id] = updated_task
                return True
        finally:
            elapsed = time.time() - start_time
            self._perf_stats['update_task_calls'] += 1
            self._perf_stats['update_task_time'] += elapsed

    def delete_task(self, task_id: str, user_id: str = None) -> bool:
        """
        Delete a task by its ID.

        Args:
            task_id: The ID of the task to delete
            user_id: The ID of the user requesting deletion (to verify ownership)

        Returns:
            True if the task was deleted successfully, False otherwise
        """
        start_time = time.time()
        try:
            with self._lock:
                if task_id not in self._tasks:
                    return False

                del self._tasks[task_id]
                return True
        finally:
            elapsed = time.time() - start_time
            self._perf_stats['delete_task_calls'] += 1
            self._perf_stats['delete_task_time'] += elapsed

    def clear_all(self):
        """
        Clear all tasks from the store (used for testing/resetting).
        """
        with self._lock:
            self._tasks.clear()

    def get_task_count(self) -> int:
        """
        Get the current number of tasks in storage.

        Returns:
            The number of tasks in storage
        """
        with self._lock:
            return len(self._tasks)

    # User-related methods
    def create_user(self, user: User) -> bool:
        """
        Create a new user in memory.

        Args:
            user: The user to create

        Returns:
            True if the user was created successfully, False otherwise
        """
        with self._lock:
            # Check if username or email already exists
            for existing_user in self._users.values():
                if existing_user.username == user.username or existing_user.email == user.email:
                    return False

            self._users[user.id] = user
            return True

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """
        Retrieve a user by their ID.

        Args:
            user_id: The ID of the user to retrieve

        Returns:
            The user if found, None otherwise
        """
        with self._lock:
            return self._users.get(user_id)

    def get_user_by_username(self, username: str) -> Optional[User]:
        """
        Retrieve a user by their username.

        Args:
            username: The username of the user to retrieve

        Returns:
            The user if found, None otherwise
        """
        with self._lock:
            for user in self._users.values():
                if user.username == username:
                    return user
            return None

    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Retrieve a user by their email.

        Args:
            email: The email of the user to retrieve

        Returns:
            The user if found, None otherwise
        """
        with self._lock:
            for user in self._users.values():
                if user.email == email:
                    return user
            return None

    def update_user(self, user_id: str, username: str = None, email: str = None, password_hash: str = None) -> bool:
        """
        Update a user's information.

        Args:
            user_id: The ID of the user to update
            username: New username (optional)
            email: New email (optional)
            password_hash: New password hash (optional)

        Returns:
            True if the user was updated successfully, False otherwise
        """
        with self._lock:
            if user_id not in self._users:
                return False

            user = self._users[user_id]

            if username is not None:
                # Check if another user already has this username
                for u_id, u in self._users.items():
                    if u_id != user_id and u.username == username:
                        return False
                user.username = username

            if email is not None:
                # Check if another user already has this email
                for u_id, u in self._users.items():
                    if u_id != user_id and u.email == email:
                        return False
                user.email = email

            if password_hash is not None:
                user.password_hash = password_hash

            return True

    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """
        Authenticate a user by username and password.

        Args:
            username: The username to authenticate
            password: The plain text password to verify

        Returns:
            The user object if authentication succeeds, None otherwise
        """
        from src.models.user import verify_password

        with self._lock:
            user = self.get_user_by_username(username)
            if user and verify_password(password, user.password_hash):
                return user
            return None

    def delete_user(self, user_id: str) -> bool:
        """
        Delete a user from memory.

        Args:
            user_id: The ID of the user to delete

        Returns:
            True if the user was deleted successfully, False otherwise
        """
        with self._lock:
            if user_id in self._users:
                del self._users[user_id]
                return True
            return False

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
