import argparse
import sys
import os

# Add the project root to the Python path so imports work
if __name__ == "__main__" and __package__ is None:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models.task import TaskCreate, TaskUpdate
from src.models.user import UserCreate, UserLogin
from src.storage.sqlite_storage import SQLiteStorage
from src.services.cli_todo_service import CLITodoService
from src.config import settings


class TodoCLI:
    """
    Command-line interface for the todo application.
    Provides clear, intuitive command-line options with consistent UX patterns
    as required by the constitution.
    """

    def __init__(self):
        self.storage = SQLiteStorage(settings.db_path)
        self.service = CLITodoService(self.storage)
        self.parser = self._create_parser()

    def _create_parser(self) -> argparse.ArgumentParser:
        """Create and configure the argument parser."""
        parser = argparse.ArgumentParser(
            prog="todo",
            description="Command-line todo application",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  %(prog)s register --username john --email john@example.com --password secret123
  %(prog)s login --username john --password secret123
  %(prog)s add "Buy groceries"
  %(prog)s list
  %(prog)s update 123e4567-e89b-12d3-a456-426614174000 "Buy weekly groceries"
  %(prog)s delete 123e4567-e89b-12d3-a456-426614174000
  %(prog)s complete 123e4567-e89b-12d3-a456-426614174000
  %(prog)s incomplete 123e4567-e89b-12d3-a456-426614174000
            """,
        )

        # Add argument for interactive mode
        parser.add_argument('-i', '--interactive', action='store_true',
                           help='Run in interactive mode with menu')

        subparsers = parser.add_subparsers(dest="command", help="Available commands")

        # Authentication commands
        register_parser = subparsers.add_parser("register", help="Register a new user")
        register_parser.add_argument("--username", required=True, help="Username for the new user")
        register_parser.add_argument("--email", required=True, help="Email for the new user")
        register_parser.add_argument("--password", required=True, help="Password for the new user")

        login_parser = subparsers.add_parser("login", help="Login to your account")
        login_parser.add_argument("--username", required=True, help="Your username")
        login_parser.add_argument("--password", required=True, help="Your password")

        logout_parser = subparsers.add_parser("logout", help="Logout from your account")

        # Task commands (require authentication)
        add_parser = subparsers.add_parser("add", help="Add a new task")
        add_parser.add_argument("description", nargs="+", help="Task description")

        # List command
        subparsers.add_parser("list", help="List all your tasks")

        # Update command
        update_parser = subparsers.add_parser("update", help="Update a task")
        update_parser.add_argument("task_id", help="Task ID to update")
        update_parser.add_argument(
            "description", nargs="+", help="New task description"
        )

        # Delete command
        subparsers.add_parser("delete", help="Delete a task").add_argument(
            "task_id", help="Task ID to delete"
        )

        # Complete command
        subparsers.add_parser("complete", help="Mark task as complete").add_argument(
            "task_id", help="Task ID to mark complete"
        )

        # Incomplete command
        subparsers.add_parser(
            "incomplete", help="Mark task as incomplete"
        ).add_argument("task_id", help="Task ID to mark incomplete")

        # Count command
        subparsers.add_parser("count", help="Count total tasks")

        return parser

    def run(self, args=None):
        """Run the CLI application with the provided arguments."""
        if args is None:
            args = sys.argv[1:]

        # Check if we should run in interactive mode
        if not args or (len(args) == 1 and args[0] in ['-i', '--interactive']):
            self.run_interactive()
        else:
            # Parse and execute the command
            try:
                parsed_args = self.parser.parse_args(args)

                if parsed_args.command == "register":
                    self.register_user(parsed_args.username, parsed_args.email, parsed_args.password)
                elif parsed_args.command == "login":
                    self.login_user(parsed_args.username, parsed_args.password)
                elif parsed_args.command == "logout":
                    self.logout_user()
                elif parsed_args.command == "add":
                    if not self.service.current_user_id:
                        print("Error: You must be logged in to add a task.", file=sys.stderr)
                        sys.exit(1)
                    description = " ".join(parsed_args.description)
                    self.add_task(description)
                elif parsed_args.command == "list":
                    if not self.service.current_user_id:
                        print("Error: You must be logged in to list tasks.", file=sys.stderr)
                        sys.exit(1)
                    self.list_tasks()
                elif parsed_args.command == "update":
                    if not self.service.current_user_id:
                        print("Error: You must be logged in to update a task.", file=sys.stderr)
                        sys.exit(1)
                    description = " ".join(parsed_args.description)
                    self.update_task(parsed_args.task_id, description)
                elif parsed_args.command == "delete":
                    if not self.service.current_user_id:
                        print("Error: You must be logged in to delete a task.", file=sys.stderr)
                        sys.exit(1)
                    self.delete_task(parsed_args.task_id)
                elif parsed_args.command == "complete":
                    if not self.service.current_user_id:
                        print("Error: You must be logged in to mark a task complete.", file=sys.stderr)
                        sys.exit(1)
                    self.mark_task_complete(parsed_args.task_id)
                elif parsed_args.command == "incomplete":
                    if not self.service.current_user_id:
                        print("Error: You must be logged in to mark a task incomplete.", file=sys.stderr)
                        sys.exit(1)
                    self.mark_task_incomplete(parsed_args.task_id)
                elif parsed_args.command == "count":
                    if not self.service.current_user_id:
                        print("Error: You must be logged in to count tasks.", file=sys.stderr)
                        sys.exit(1)
                    self.count_tasks()
                else:
                    self.parser.print_help()
            except Exception as e:
                print(f"Error: {str(e)}", file=sys.stderr)
                sys.exit(1)

    def run_interactive(self):
        """Run the CLI in interactive mode with a menu loop."""
        print("Welcome to the Interactive Todo Application!")
        print("Type 'help' for available commands or 'quit' to exit.\n")

        while True:
            try:
                # Display menu
                print("\n--- Todo Menu ---")
                print("1. Add Task (a)")
                print("2. List Tasks (l)")
                print("3. Update Task (u)")
                print("4. Delete Task (d)")
                print("5. Mark Task Complete (c)")
                print("6. Mark Task Incomplete (i)")
                print("7. Count Tasks (ct)")
                print("8. Help (h)")
                print("9. Quit (q)")

                choice = input("\nEnter your choice: ").strip().lower()

                if choice in ['q', 'quit', 'exit']:
                    print("Goodbye!")
                    break
                elif choice in ['1', 'a', 'add']:
                    self.interactive_add_task()
                elif choice in ['2', 'l', 'list']:
                    self.list_tasks()
                elif choice in ['3', 'u', 'update']:
                    self.interactive_update_task()
                elif choice in ['4', 'd', 'delete']:
                    self.interactive_delete_task()
                elif choice in ['5', 'c', 'complete']:
                    self.interactive_mark_complete()
                elif choice in ['6', 'i', 'incomplete']:
                    self.interactive_mark_incomplete()
                elif choice in ['7', 'ct', 'count']:
                    self.count_tasks()
                elif choice in ['8', 'h', 'help']:
                    self.show_interactive_help()
                else:
                    print("Invalid choice. Please try again.")

            except KeyboardInterrupt:
                print("\n\nOperation cancelled by user.")
                break
            except Exception as e:
                print(f"Error: {str(e)}", file=sys.stderr)

    def interactive_add_task(self):
        """Interactive task addition."""
        try:
            description = input("Enter task description: ").strip()
            if not description:
                print("Task description cannot be empty.")
                return

            task_create = TaskCreate(description=description)
            task = self.service.add_task(task_create)

            if task:
                print("Task added successfully!")
                print(f"ID: {task.id}")
                print(f"Description: {task.description}")
                print(f"Status: {task.status}")
            else:
                print("Error: Failed to add task. Task limit may have been reached.")
        except KeyboardInterrupt:
            print("\nTask addition cancelled.")

    def interactive_update_task(self):
        """Interactive task update."""
        try:
            # First, list all tasks to help user identify the ID
            tasks = self.service.get_all_tasks()
            if not tasks:
                print("No tasks found to update.")
                return

            print("\nCurrent tasks:")
            for task in tasks:
                status_symbol = "X" if task.status == "complete" else "O"
                print(f"[{status_symbol}] ID: {task.id}")
                print(f"    Description: {task.description}")
                print()

            task_id = input("Enter task ID to update: ").strip()
            if not task_id:
                print("Task ID cannot be empty.")
                return

            # Find and display the current task
            task = next((t for t in tasks if t.id == task_id), None)
            if not task:
                print(f"Error: Task with ID {task_id} not found.")
                return

            print(f"Current task: {task.description}")
            new_description = input("Enter new description: ").strip()
            if not new_description:
                print("Task description cannot be empty.")
                return

            task_update = TaskUpdate(description=new_description)
            updated_task = self.service.update_task(task_id, task_update)

            if updated_task:
                print("Task updated successfully!")
                print(f"ID: {updated_task.id}")
                print(f"Description: {updated_task.description}")
                print(f"Status: {updated_task.status}")
            else:
                print(f"Error: Task with ID {task_id} not found.")
        except KeyboardInterrupt:
            print("\nTask update cancelled.")

    def interactive_delete_task(self):
        """Interactive task deletion."""
        try:
            # First, list all tasks to help user identify the ID
            tasks = self.service.get_all_tasks()
            if not tasks:
                print("No tasks found to delete.")
                return

            print("\nCurrent tasks:")
            for task in tasks:
                status_symbol = "X" if task.status == "complete" else "O"
                print(f"[{status_symbol}] ID: {task.id}")
                print(f"    Description: {task.description}")
                print()

            task_id = input("Enter task ID to delete: ").strip()
            if not task_id:
                print("Task ID cannot be empty.")
                return

            # Find and display the task to be deleted
            task = next((t for t in tasks if t.id == task_id), None)
            if not task:
                print(f"Error: Task with ID {task_id} not found.")
                return

            print(f"You are about to delete: {task.description}")
            confirm = input("Are you sure? (yes/no): ").strip().lower()

            if confirm in ['y', 'yes']:
                success = self.service.delete_task(task_id)

                if success:
                    print(f"Task with ID {task_id} deleted successfully!")
                else:
                    print(f"Error: Task with ID {task_id} not found.")
            else:
                print("Deletion cancelled.")
        except KeyboardInterrupt:
            print("\nTask deletion cancelled.")

    def interactive_mark_complete(self):
        """Interactive mark task complete."""
        try:
            # First, list all tasks to help user identify the ID
            tasks = self.service.get_all_tasks()
            if not tasks:
                print("No tasks found.")
                return

            print("\nCurrent tasks:")
            for task in tasks:
                status_symbol = "X" if task.status == "complete" else "O"
                print(f"[{status_symbol}] ID: {task.id}")
                print(f"    Description: {task.description}")
                print()

            task_id = input("Enter task ID to mark complete: ").strip()
            if not task_id:
                print("Task ID cannot be empty.")
                return

            task = self.service.mark_task_complete(task_id)

            if task:
                print(f"Task with ID {task_id} marked as complete!")
                print(f"Description: {task.description}")
            else:
                print(f"Error: Task with ID {task_id} not found.")
        except KeyboardInterrupt:
            print("\nOperation cancelled.")

    def interactive_mark_incomplete(self):
        """Interactive mark task incomplete."""
        try:
            # First, list all tasks to help user identify the ID
            tasks = self.service.get_all_tasks()
            if not tasks:
                print("No tasks found.")
                return

            print("\nCurrent tasks:")
            for task in tasks:
                status_symbol = "X" if task.status == "complete" else "O"
                print(f"[{status_symbol}] ID: {task.id}")
                print(f"    Description: {task.description}")
                print()

            task_id = input("Enter task ID to mark incomplete: ").strip()
            if not task_id:
                print("Task ID cannot be empty.")
                return

            task = self.service.mark_task_incomplete(task_id)

            if task:
                print(f"Task with ID {task_id} marked as incomplete!")
                print(f"Description: {task.description}")
            else:
                print(f"Error: Task with ID {task_id} not found.")
        except KeyboardInterrupt:
            print("\nOperation cancelled.")

    def show_interactive_help(self):
        """Display help for interactive mode."""
        print("\n--- Interactive Mode Help ---")
        print("Commands available:")
        print("  Add Task: Add a new todo item")
        print("  List Tasks: Show all tasks")
        print("  Update Task: Modify an existing task's description")
        print("  Delete Task: Remove a task (with confirmation)")
        print("  Mark Complete: Mark a task as completed")
        print("  Mark Incomplete: Mark a task as not completed")
        print("  Count Tasks: Show total number of tasks")
        print("  Help: Show this help message")
        print("  Quit: Exit the application")

    def add_task(self, description: str):
        """Add a new task with the given description."""
        if not description or len(description.strip()) == 0:
            print("Error: Task description cannot be empty.", file=sys.stderr)
            return

        task_create = TaskCreate(description=description)
        task = self.service.add_task(task_create)

        if task:
            print("Task added successfully!")
            print(f"ID: {task.id}")
            print(f"Description: {task.description}")
            print(f"Status: {task.status}")
            print(f"Created: {task.created_date.strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            print(
                "Error: Failed to add task. Task limit may have been reached.",
                file=sys.stderr,
            )

    def list_tasks(self):
        """List all tasks in the system."""
        tasks = self.service.get_all_tasks()

        if not tasks:
            print("No tasks found.")
            return

        print(f"Total tasks: {len(tasks)}")
        print("-" * 100)

        for task in tasks:
            status_symbol = "X" if task.status == "complete" else "O"
            created_str = task.created_date.strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{status_symbol}] ID: {task.id}")
            print(f"    Description: {task.description}")
            print(f"    Status: {task.status} | Created: {created_str}")
            print()

    def update_task(self, task_id: str, description: str):
        """Update an existing task's description."""
        if not description or len(description.strip()) == 0:
            print("Error: Task description cannot be empty.", file=sys.stderr)
            return

        task_update = TaskUpdate(description=description)
        updated_task = self.service.update_task(task_id, task_update)

        if updated_task:
            print("Task updated successfully!")
            print(f"ID: {updated_task.id}")
            print(f"Description: {updated_task.description}")
            print(f"Status: {updated_task.status}")
        else:
            print(f"Error: Task with ID {task_id} not found.", file=sys.stderr)

    def delete_task(self, task_id: str):
        """Delete a task by its ID."""
        success = self.service.delete_task(task_id)

        if success:
            print(f"Task with ID {task_id} deleted successfully!")
        else:
            print(f"Error: Task with ID {task_id} not found.", file=sys.stderr)

    def mark_task_complete(self, task_id: str):
        """Mark a task as complete."""
        task = self.service.mark_task_complete(task_id)

        if task:
            print(f"Task with ID {task_id} marked as complete!")
            print(f"Description: {task.description}")
        else:
            print(f"Error: Task with ID {task_id} not found.", file=sys.stderr)

    def mark_task_incomplete(self, task_id: str):
        """Mark a task as incomplete."""
        task = self.service.mark_task_incomplete(task_id)

        if task:
            print(f"Task with ID {task_id} marked as incomplete!")
            print(f"Description: {task.description}")
        else:
            print(f"Error: Task with ID {task_id} not found.", file=sys.stderr)

    def count_tasks(self):
        """Count the total number of tasks."""
        count = self.service.get_task_count()
        print(f"Total tasks: {count}")


    def register_user(self, username: str, email: str, password: str):
        """Register a new user."""
        try:
            user_create = UserCreate(username=username, email=email, password=password)
            user = self.service.register_user(user_create)

            if user:
                print("Registration successful!")
                print(f"User ID: {user.id}")
                print(f"Username: {user.username}")
                print(f"Email: {user.email}")
            else:
                print("Error: Failed to register user. Username or email may already exist.", file=sys.stderr)
        except Exception as e:
            print(f"Error during registration: {str(e)}", file=sys.stderr)

    def login_user(self, username: str, password: str):
        """Login a user."""
        try:
            user_login = UserLogin(username=username, password=password)
            result = self.service.login_user(user_login)

            if result:
                print("Login successful!")
                print(f"Welcome, {result['username']}!")
            else:
                print("Error: Login failed. Invalid username or password.", file=sys.stderr)
        except Exception as e:
            print(f"Error during login: {str(e)}", file=sys.stderr)

    def logout_user(self):
        """Logout the current user."""
        try:
            success = self.service.logout_user()
            if success:
                print("Logged out successfully!")
            else:
                print("You were not logged in.")
        except Exception as e:
            print(f"Error during logout: {str(e)}", file=sys.stderr)

    def run_interactive(self):
        """Run the CLI in interactive mode with a menu loop."""
        print("Welcome to the Interactive Todo Application!")

        # Check if user is logged in
        if not self.service.current_user_id:
            print("You are not logged in. Please register or login first.")
            print("Options: 'register', 'login', 'quit'\n")

            while not self.service.current_user_id:
                action = input("Choose action (register/login/quit): ").strip().lower()

                if action == 'register':
                    username = input("Enter username: ").strip()
                    email = input("Enter email: ").strip()
                    password = input("Enter password: ").strip()
                    self.register_user(username, email, password)
                elif action == 'login':
                    username = input("Enter username: ").strip()
                    password = input("Enter password: ").strip()
                    self.login_user(username, password)
                elif action == 'quit':
                    print("Goodbye!")
                    return
                else:
                    print("Invalid option. Please choose 'register', 'login', or 'quit'.")

        print("Type 'help' for available commands or 'quit' to exit.\n")

        while True:
            try:
                # Display menu
                print("\n--- Todo Menu ---")
                print("1. Add Task (a)")
                print("2. List Tasks (l)")
                print("3. Update Task (u)")
                print("4. Delete Task (d)")
                print("5. Mark Task Complete (c)")
                print("6. Mark Task Incomplete (i)")
                print("7. Count Tasks (ct)")
                print("8. Logout (lo)")
                print("9. Help (h)")
                print("10. Quit (q)")

                choice = input("\nEnter your choice: ").strip().lower()

                if choice in ['q', 'quit', 'exit']:
                    print("Goodbye!")
                    break
                elif choice in ['1', 'a', 'add']:
                    self.interactive_add_task()
                elif choice in ['2', 'l', 'list']:
                    self.list_tasks()
                elif choice in ['3', 'u', 'update']:
                    self.interactive_update_task()
                elif choice in ['4', 'd', 'delete']:
                    self.interactive_delete_task()
                elif choice in ['5', 'c', 'complete']:
                    self.interactive_mark_complete()
                elif choice in ['6', 'i', 'incomplete']:
                    self.interactive_mark_incomplete()
                elif choice in ['7', 'ct', 'count']:
                    self.count_tasks()
                elif choice in ['8', 'lo', 'logout']:
                    self.logout_user()
                    print("Logging out...")
                    return  # Exit interactive mode after logout
                elif choice in ['9', 'h', 'help']:
                    self.show_interactive_help()
                else:
                    print("Invalid choice. Please try again.")

            except KeyboardInterrupt:
                print("\n\nOperation cancelled by user.")
                break
            except Exception as e:
                print(f"Error: {str(e)}", file=sys.stderr)

    def interactive_add_task(self):
        """Interactive task addition."""
        try:
            if not self.service.current_user_id:
                print("You must be logged in to add a task.")
                return

            description = input("Enter task description: ").strip()
            if not description:
                print("Task description cannot be empty.")
                return

            task_create = TaskCreate(description=description)
            task = self.service.add_task(task_create)

            if task:
                print("Task added successfully!")
                print(f"ID: {task.id}")
                print(f"Description: {task.description}")
                print(f"Status: {task.status}")
            else:
                print("Error: Failed to add task. Task limit may have been reached.")
        except KeyboardInterrupt:
            print("\nTask addition cancelled.")

    def interactive_update_task(self):
        """Interactive task update."""
        try:
            if not self.service.current_user_id:
                print("You must be logged in to update a task.")
                return

            # First, list all tasks to help user identify the ID
            tasks = self.service.get_all_tasks()
            if not tasks:
                print("No tasks found to update.")
                return

            print("\nCurrent tasks:")
            for task in tasks:
                status_symbol = "X" if task.status == "complete" else "O"
                print(f"[{status_symbol}] ID: {task.id}")
                print(f"    Description: {task.description}")
                print()

            task_id = input("Enter task ID to update: ").strip()
            if not task_id:
                print("Task ID cannot be empty.")
                return

            # Find and display the current task
            task = next((t for t in tasks if t.id == task_id), None)
            if not task:
                print(f"Error: Task with ID {task_id} not found.")
                return

            print(f"Current task: {task.description}")
            new_description = input("Enter new description: ").strip()
            if not new_description:
                print("Task description cannot be empty.")
                return

            task_update = TaskUpdate(description=new_description)
            updated_task = self.service.update_task(task_id, task_update)

            if updated_task:
                print("Task updated successfully!")
                print(f"ID: {updated_task.id}")
                print(f"Description: {updated_task.description}")
                print(f"Status: {updated_task.status}")
            else:
                print(f"Error: Task with ID {task_id} not found.")
        except KeyboardInterrupt:
            print("\nTask update cancelled.")

    def interactive_delete_task(self):
        """Interactive task deletion."""
        try:
            if not self.service.current_user_id:
                print("You must be logged in to delete a task.")
                return

            # First, list all tasks to help user identify the ID
            tasks = self.service.get_all_tasks()
            if not tasks:
                print("No tasks found to delete.")
                return

            print("\nCurrent tasks:")
            for task in tasks:
                status_symbol = "X" if task.status == "complete" else "O"
                print(f"[{status_symbol}] ID: {task.id}")
                print(f"    Description: {task.description}")
                print()

            task_id = input("Enter task ID to delete: ").strip()
            if not task_id:
                print("Task ID cannot be empty.")
                return

            # Find and display the task to be deleted
            task = next((t for t in tasks if t.id == task_id), None)
            if not task:
                print(f"Error: Task with ID {task_id} not found.")
                return

            print(f"You are about to delete: {task.description}")
            confirm = input("Are you sure? (yes/no): ").strip().lower()

            if confirm in ['y', 'yes']:
                success = self.service.delete_task(task_id)

                if success:
                    print(f"Task with ID {task_id} deleted successfully!")
                else:
                    print(f"Error: Task with ID {task_id} not found.")
            else:
                print("Deletion cancelled.")
        except KeyboardInterrupt:
            print("\nTask deletion cancelled.")

    def interactive_mark_complete(self):
        """Interactive mark task complete."""
        try:
            if not self.service.current_user_id:
                print("You must be logged in to mark a task complete.")
                return

            # First, list all tasks to help user identify the ID
            tasks = self.service.get_all_tasks()
            if not tasks:
                print("No tasks found.")
                return

            print("\nCurrent tasks:")
            for task in tasks:
                status_symbol = "X" if task.status == "complete" else "O"
                print(f"[{status_symbol}] ID: {task.id}")
                print(f"    Description: {task.description}")
                print()

            task_id = input("Enter task ID to mark complete: ").strip()
            if not task_id:
                print("Task ID cannot be empty.")
                return

            task = self.service.mark_task_complete(task_id)

            if task:
                print(f"Task with ID {task_id} marked as complete!")
                print(f"Description: {task.description}")
            else:
                print(f"Error: Task with ID {task_id} not found.")
        except KeyboardInterrupt:
            print("\nOperation cancelled.")

    def interactive_mark_incomplete(self):
        """Interactive mark task incomplete."""
        try:
            if not self.service.current_user_id:
                print("You must be logged in to mark a task incomplete.")
                return

            # First, list all tasks to help user identify the ID
            tasks = self.service.get_all_tasks()
            if not tasks:
                print("No tasks found.")
                return

            print("\nCurrent tasks:")
            for task in tasks:
                status_symbol = "X" if task.status == "complete" else "O"
                print(f"[{status_symbol}] ID: {task.id}")
                print(f"    Description: {task.description}")
                print()

            task_id = input("Enter task ID to mark incomplete: ").strip()
            if not task_id:
                print("Task ID cannot be empty.")
                return

            task = self.service.mark_task_incomplete(task_id)

            if task:
                print(f"Task with ID {task_id} marked as incomplete!")
                print(f"Description: {task.description}")
            else:
                print(f"Error: Task with ID {task_id} not found.")
        except KeyboardInterrupt:
            print("\nOperation cancelled.")

    def show_interactive_help(self):
        """Display help for interactive mode."""
        print("\n--- Interactive Mode Help ---")
        print("Commands available:")
        print("  Add Task: Add a new todo item")
        print("  List Tasks: Show all your tasks")
        print("  Update Task: Modify an existing task's description")
        print("  Delete Task: Remove a task (with confirmation)")
        print("  Mark Complete: Mark a task as completed")
        print("  Mark Incomplete: Mark a task as not completed")
        print("  Count Tasks: Show total number of your tasks")
        print("  Logout: Log out of your account")
        print("  Help: Show this help message")
        print("  Quit: Exit the application")

    def add_task(self, description: str):
        """Add a new task with the given description."""
        if not self.service.current_user_id:
            print("You must be logged in to add a task.", file=sys.stderr)
            return

        if not description or len(description.strip()) == 0:
            print("Error: Task description cannot be empty.", file=sys.stderr)
            return

        task_create = TaskCreate(description=description)
        task = self.service.add_task(task_create)

        if task:
            print("Task added successfully!")
            print(f"ID: {task.id}")
            print(f"Description: {task.description}")
            print(f"Status: {task.status}")
            print(f"Created: {task.created_date.strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            print(
                "Error: Failed to add task. Task limit may have been reached.",
                file=sys.stderr,
            )

    def list_tasks(self):
        """List all tasks in the system."""
        if not self.service.current_user_id:
            print("You must be logged in to list tasks.", file=sys.stderr)
            return

        tasks = self.service.get_all_tasks()

        if not tasks:
            print("No tasks found.")
            return

        print(f"Total tasks: {len(tasks)}")
        print("-" * 100)

        for task in tasks:
            status_symbol = "X" if task.status == "complete" else "O"
            created_str = task.created_date.strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{status_symbol}] ID: {task.id}")
            print(f"    Description: {task.description}")
            print(f"    Status: {task.status} | Created: {created_str}")
            print()

    def update_task(self, task_id: str, description: str):
        """Update an existing task's description."""
        if not self.service.current_user_id:
            print("You must be logged in to update a task.", file=sys.stderr)
            return

        if not description or len(description.strip()) == 0:
            print("Error: Task description cannot be empty.", file=sys.stderr)
            return

        task_update = TaskUpdate(description=description)
        updated_task = self.service.update_task(task_id, task_update)

        if updated_task:
            print("Task updated successfully!")
            print(f"ID: {updated_task.id}")
            print(f"Description: {updated_task.description}")
            print(f"Status: {updated_task.status}")
        else:
            print(f"Error: Task with ID {task_id} not found.", file=sys.stderr)

    def delete_task(self, task_id: str):
        """Delete a task by its ID."""
        if not self.service.current_user_id:
            print("You must be logged in to delete a task.", file=sys.stderr)
            return

        success = self.service.delete_task(task_id)

        if success:
            print(f"Task with ID {task_id} deleted successfully!")
        else:
            print(f"Error: Task with ID {task_id} not found.", file=sys.stderr)

    def mark_task_complete(self, task_id: str):
        """Mark a task as complete."""
        if not self.service.current_user_id:
            print("You must be logged in to mark a task complete.", file=sys.stderr)
            return

        task = self.service.mark_task_complete(task_id)

        if task:
            print(f"Task with ID {task_id} marked as complete!")
            print(f"Description: {task.description}")
        else:
            print(f"Error: Task with ID {task_id} not found.", file=sys.stderr)

    def mark_task_incomplete(self, task_id: str):
        """Mark a task as incomplete."""
        if not self.service.current_user_id:
            print("You must be logged in to mark a task incomplete.", file=sys.stderr)
            return

        task = self.service.mark_task_incomplete(task_id)

        if task:
            print(f"Task with ID {task_id} marked as incomplete!")
            print(f"Description: {task.description}")
        else:
            print(f"Error: Task with ID {task_id} not found.", file=sys.stderr)

    def count_tasks(self):
        """Count the total number of tasks."""
        if not self.service.current_user_id:
            print("You must be logged in to count tasks.", file=sys.stderr)
            return

        count = self.service.get_task_count()
        print(f"Total tasks: {count}")


def main():
    """Main entry point for the CLI application."""
    cli = TodoCLI()
    cli.run()


if __name__ == "__main__":
    cli = TodoCLI()
    cli.run()
