"""Database models and setup for the todo application."""

import sqlite3
import json
from datetime import datetime
from typing import List, Optional
from src.models.task import Task
from src.models.user import User, hash_password, verify_password
import os


class TaskDB:
    """SQLite database handler for task and user storage."""

    def __init__(self, db_path: str = "todo_app.db"):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        """Initialize the database and create tables if they don't exist."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Create users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_date TEXT NOT NULL
            )
        """)

        # Create tasks table with user_id foreign key
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id TEXT PRIMARY KEY,
                description TEXT NOT NULL,
                status TEXT NOT NULL,
                created_date TEXT NOT NULL,
                user_id TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)

        conn.commit()
        conn.close()

    def add_task(self, task: Task, user_id: str) -> bool:
        """Add a task to the database."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO tasks (id, description, status, created_date, user_id)
                VALUES (?, ?, ?, ?, ?)
            """, (task.id, task.description, task.status, task.created_date.isoformat(), user_id))

            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            # Task with this ID already exists
            return False
        except Exception as e:
            print(f"Error adding task to database: {e}")
            return False

    def get_task(self, task_id: str) -> Optional[Task]:
        """Get a specific task by ID."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT id, description, status, created_date FROM tasks WHERE id = ?", (task_id,))
        row = cursor.fetchone()

        conn.close()

        if row:
            # Create Task object from database row
            return Task(
                id=row[0],
                description=row[1],
                status=row[2],
                created_date=datetime.fromisoformat(row[3])
            )
        return None

    def get_tasks_by_user(self, user_id: str) -> List[Task]:
        """Get all tasks for a specific user."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT id, description, status, created_date FROM tasks WHERE user_id = ? ORDER BY created_date DESC", (user_id,))
        rows = cursor.fetchall()

        conn.close()

        tasks = []
        for row in rows:
            task = Task(
                id=row[0],
                description=row[1],
                status=row[2],
                created_date=datetime.fromisoformat(row[3])
            )
            tasks.append(task)

        return tasks

    def get_all_tasks(self) -> List[Task]:
        """Get all tasks from the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT id, description, status, created_date FROM tasks ORDER BY created_date DESC")
        rows = cursor.fetchall()

        conn.close()

        tasks = []
        for row in rows:
            task = Task(
                id=row[0],
                description=row[1],
                status=row[2],
                created_date=datetime.fromisoformat(row[3])
            )
            tasks.append(task)

        return tasks

    def update_task(self, task_id: str, task: Task) -> bool:
        """Update a task in the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE tasks
            SET description = ?, status = ?, created_date = ?
            WHERE id = ?
        """, (task.description, task.status, task.created_date.isoformat(), task_id))

        rows_affected = cursor.rowcount
        conn.commit()
        conn.close()

        return rows_affected > 0

    def delete_task(self, task_id: str, user_id: str = None) -> bool:
        """Delete a task from the database. If user_id is provided, verify ownership."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        if user_id:
            # Verify that the task belongs to the user
            cursor.execute("SELECT user_id FROM tasks WHERE id = ?", (task_id,))
            result = cursor.fetchone()
            if not result or result[0] != user_id:
                conn.close()
                return False  # Task doesn't exist or doesn't belong to user

        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        rows_affected = cursor.rowcount

        conn.commit()
        conn.close()

        return rows_affected > 0

    def clear_all_tasks(self) -> bool:
        """Clear all tasks from the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("DELETE FROM tasks")
        conn.commit()
        conn.close()

        return True

    def get_task_count(self) -> int:
        """Get the count of tasks in the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM tasks")
        count = cursor.fetchone()[0]

        conn.close()
        return count

    # User-related methods
    def create_user(self, user: User) -> bool:
        """Create a new user in the database."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO users (id, username, email, password_hash, created_date)
                VALUES (?, ?, ?, ?, ?)
            """, (user.id, user.username, user.email, user.password_hash, user.created_date.isoformat()))

            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            # User with this username or email already exists
            return False
        except Exception as e:
            print(f"Error creating user in database: {e}")
            return False

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get a user by ID."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT id, username, email, password_hash, created_date FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()

        conn.close()

        if row:
            return User(
                id=row[0],
                username=row[1],
                email=row[2],
                password_hash=row[3],
                created_date=datetime.fromisoformat(row[4])
            )
        return None

    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get a user by username."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT id, username, email, password_hash, created_date FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()

        conn.close()

        if row:
            return User(
                id=row[0],
                username=row[1],
                email=row[2],
                password_hash=row[3],
                created_date=datetime.fromisoformat(row[4])
            )
        return None

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get a user by email."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT id, username, email, password_hash, created_date FROM users WHERE email = ?", (email,))
        row = cursor.fetchone()

        conn.close()

        if row:
            return User(
                id=row[0],
                username=row[1],
                email=row[2],
                password_hash=row[3],
                created_date=datetime.fromisoformat(row[4])
            )
        return None

    def update_user(self, user_id: str, username: str = None, email: str = None, password_hash: str = None) -> bool:
        """Update a user's information."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Build the update query dynamically based on provided fields
        updates = []
        params = []

        if username:
            updates.append("username = ?")
            params.append(username)
        if email:
            updates.append("email = ?")
            params.append(email)
        if password_hash:
            updates.append("password_hash = ?")
            params.append(password_hash)

        if not updates:
            conn.close()
            return False  # Nothing to update

        query = f"UPDATE users SET {', '.join(updates)} WHERE id = ?"
        params.append(user_id)

        cursor.execute(query, tuple(params))
        rows_affected = cursor.rowcount

        conn.commit()
        conn.close()

        return rows_affected > 0

    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """Authenticate a user by username and password."""
        user = self.get_user_by_username(username)
        if user and verify_password(password, user.password_hash):
            return user
        return None

    def delete_user(self, user_id: str) -> bool:
        """Delete a user and all their tasks."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Delete user's tasks first (due to foreign key constraint)
        cursor.execute("DELETE FROM tasks WHERE user_id = ?", (user_id,))

        # Delete the user
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        rows_affected = cursor.rowcount

        conn.commit()
        conn.close()

        return rows_affected > 0