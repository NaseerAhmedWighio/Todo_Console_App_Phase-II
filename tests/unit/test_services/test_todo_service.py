import pytest
from datetime import datetime
from unittest.mock import Mock
from src.models.task import Task, TaskCreate, TaskUpdate
from src.services.todo_service import TodoService
from src.storage.in_memory import InMemoryStorage


def test_add_task_success():
    """Test adding a task successfully."""
    storage = InMemoryStorage()
    service = TodoService(storage)

    task_create = TaskCreate(description="Test description")

    result = service.add_task(task_create)

    assert result is not None
    assert result.description == "Test description"
    assert result.status == "incomplete"
    assert len(storage._tasks) == 1


def test_add_task_failure():
    """Test adding a task when storage fails."""
    storage = Mock(spec=InMemoryStorage)
    storage.add_task.return_value = False
    service = TodoService(storage)

    task_create = TaskCreate(description="Test description")

    result = service.add_task(task_create)

    assert result is None


def test_get_task_found():
    """Test retrieving an existing task."""
    storage = InMemoryStorage()
    service = TodoService(storage)

    task = Task(
        id="test-id",
        description="Test description",
        status="incomplete",
        created_date=datetime.now()
    )
    storage.add_task(task)

    result = service.get_task("test-id")

    assert result is not None
    assert result.id == "test-id"
    assert result.description == "Test description"


def test_get_task_not_found():
    """Test retrieving a non-existing task."""
    storage = InMemoryStorage()
    service = TodoService(storage)

    result = service.get_task("nonexistent-id")

    assert result is None


def test_get_all_tasks():
    """Test retrieving all tasks."""
    storage = InMemoryStorage()
    service = TodoService(storage)

    task1 = Task(
        id="test-id-1",
        description="Test description 1",
        status="incomplete",
        created_date=datetime.now()
    )
    task2 = Task(
        id="test-id-2",
        description="Test description 2",
        status="complete",
        created_date=datetime.now()
    )

    storage.add_task(task1)
    storage.add_task(task2)

    result = service.get_all_tasks()

    assert len(result) == 2
    task_ids = [task.id for task in result]
    assert "test-id-1" in task_ids
    assert "test-id-2" in task_ids


def test_get_all_tasks_empty():
    """Test retrieving all tasks when none exist."""
    storage = InMemoryStorage()
    service = TodoService(storage)

    result = service.get_all_tasks()

    assert len(result) == 0


def test_update_task_success():
    """Test updating an existing task."""
    storage = InMemoryStorage()
    service = TodoService(storage)

    original_task = Task(
        id="test-id",
        description="Original description",
        status="incomplete",
        created_date=datetime.now()
    )
    storage.add_task(original_task)

    task_update = TaskUpdate(description="Updated description")

    result = service.update_task("test-id", task_update)

    assert result is not None
    assert result.description == "Updated description"
    assert result.status == "incomplete"  # Status should be preserved


def test_update_task_not_found():
    """Test updating a non-existing task."""
    storage = InMemoryStorage()
    service = TodoService(storage)

    task_update = TaskUpdate(description="Updated description")

    result = service.update_task("nonexistent-id", task_update)

    assert result is None


def test_delete_task_success():
    """Test deleting an existing task."""
    storage = InMemoryStorage()
    service = TodoService(storage)

    task = Task(
        id="test-id",
        description="Test description",
        status="incomplete",
        created_date=datetime.now()
    )
    storage.add_task(task)

    result = service.delete_task("test-id")

    assert result is True
    assert len(storage._tasks) == 0


def test_delete_task_not_found():
    """Test deleting a non-existing task."""
    storage = InMemoryStorage()
    service = TodoService(storage)

    result = service.delete_task("nonexistent-id")

    assert result is False


def test_mark_task_complete_success():
    """Test marking a task as complete."""
    storage = InMemoryStorage()
    service = TodoService(storage)

    task = Task(
        id="test-id",
        description="Test description",
        status="incomplete",
        created_date=datetime.now()
    )
    storage.add_task(task)

    result = service.mark_task_complete("test-id")

    assert result is not None
    assert result.id == "test-id"
    assert result.status == "complete"
    assert result.description == "Test description"


def test_mark_task_complete_not_found():
    """Test marking a non-existing task as complete."""
    storage = InMemoryStorage()
    service = TodoService(storage)

    result = service.mark_task_complete("nonexistent-id")

    assert result is None


def test_mark_task_incomplete_success():
    """Test marking a task as incomplete."""
    storage = InMemoryStorage()
    service = TodoService(storage)

    task = Task(
        id="test-id",
        description="Test description",
        status="complete",
        created_date=datetime.now()
    )
    storage.add_task(task)

    result = service.mark_task_incomplete("test-id")

    assert result is not None
    assert result.id == "test-id"
    assert result.status == "incomplete"
    assert result.description == "Test description"


def test_mark_task_incomplete_not_found():
    """Test marking a non-existing task as incomplete."""
    storage = InMemoryStorage()
    service = TodoService(storage)

    result = service.mark_task_incomplete("nonexistent-id")

    assert result is None


def test_get_task_count():
    """Test getting the task count."""
    storage = InMemoryStorage()
    service = TodoService(storage)

    task1 = Task(
        id="test-id-1",
        description="Test description 1",
        status="incomplete",
        created_date=datetime.now()
    )
    task2 = Task(
        id="test-id-2",
        description="Test description 2",
        status="complete",
        created_date=datetime.now()
    )

    assert service.get_task_count() == 0

    storage.add_task(task1)
    storage.add_task(task2)

    assert service.get_task_count() == 2