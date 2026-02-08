import pytest
from datetime import datetime
from src.models.task import Task
from src.storage.in_memory import InMemoryStorage


def test_storage_initialization():
    """Test that storage initializes correctly."""
    storage = InMemoryStorage()

    assert len(storage._tasks) == 0
    assert storage._max_tasks == 1000


def test_add_task_success():
    """Test adding a task successfully."""
    storage = InMemoryStorage()

    task = Task(
        id="test-id",
        description="Test description",
        status="incomplete",
        created_date=datetime.now()
    )

    result = storage.add_task(task)

    assert result is True
    assert len(storage._tasks) == 1
    assert storage._tasks["test-id"].description == "Test description"


def test_add_duplicate_task():
    """Test that adding a duplicate task fails."""
    storage = InMemoryStorage()

    task1 = Task(
        id="test-id",
        description="Test description 1",
        status="incomplete",
        created_date=datetime.now()
    )
    task2 = Task(
        id="test-id",
        description="Test description 2",
        status="incomplete",
        created_date=datetime.now()
    )

    # Add first task
    result1 = storage.add_task(task1)
    # Try to add duplicate
    result2 = storage.add_task(task2)

    assert result1 is True
    assert result2 is False
    assert len(storage._tasks) == 1
    assert storage._tasks["test-id"].description == "Test description 1"


def test_add_task_max_limit():
    """Test that adding tasks beyond the limit fails."""
    storage = InMemoryStorage()
    storage._max_tasks = 1  # Set max to 1 for testing

    task1 = Task(
        id="test-id-1",
        description="Test description 1",
        status="incomplete",
        created_date=datetime.now()
    )
    task2 = Task(
        id="test-id-2",
        description="Test description 2",
        status="incomplete",
        created_date=datetime.now()
    )

    # Add first task (should succeed)
    result1 = storage.add_task(task1)
    # Add second task (should fail due to limit)
    result2 = storage.add_task(task2)

    assert result1 is True
    assert result2 is False
    assert len(storage._tasks) == 1


def test_get_task_found():
    """Test retrieving an existing task."""
    storage = InMemoryStorage()

    task = Task(
        id="test-id",
        description="Test description",
        status="incomplete",
        created_date=datetime.now()
    )
    storage.add_task(task)

    retrieved_task = storage.get_task("test-id")

    assert retrieved_task is not None
    assert retrieved_task.id == "test-id"
    assert retrieved_task.description == "Test description"


def test_get_task_not_found():
    """Test retrieving a non-existing task."""
    storage = InMemoryStorage()

    retrieved_task = storage.get_task("nonexistent-id")

    assert retrieved_task is None


def test_get_all_tasks():
    """Test retrieving all tasks."""
    storage = InMemoryStorage()

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

    all_tasks = storage.get_all_tasks()

    assert len(all_tasks) == 2
    task_ids = [task.id for task in all_tasks]
    assert "test-id-1" in task_ids
    assert "test-id-2" in task_ids


def test_get_all_tasks_empty():
    """Test retrieving all tasks when none exist."""
    storage = InMemoryStorage()

    all_tasks = storage.get_all_tasks()

    assert len(all_tasks) == 0


def test_update_task_success():
    """Test updating an existing task."""
    storage = InMemoryStorage()

    original_task = Task(
        id="test-id",
        description="Original description",
        status="incomplete",
        created_date=datetime.now()
    )
    storage.add_task(original_task)

    updated_task = Task(
        id="test-id",
        description="Updated description",
        status="complete",
        created_date=datetime.now()
    )

    result = storage.update_task("test-id", updated_task)

    assert result is True
    stored_task = storage.get_task("test-id")
    assert stored_task.description == "Updated description"
    assert stored_task.status == "complete"


def test_update_task_not_found():
    """Test updating a non-existing task."""
    storage = InMemoryStorage()

    updated_task = Task(
        id="test-id",
        description="Updated description",
        status="complete",
        created_date=datetime.now()
    )

    result = storage.update_task("test-id", updated_task)

    assert result is False


def test_delete_task_success():
    """Test deleting an existing task."""
    storage = InMemoryStorage()

    task = Task(
        id="test-id",
        description="Test description",
        status="incomplete",
        created_date=datetime.now()
    )
    storage.add_task(task)

    result = storage.delete_task("test-id")

    assert result is True
    assert len(storage._tasks) == 0
    assert storage.get_task("test-id") is None


def test_delete_task_not_found():
    """Test deleting a non-existing task."""
    storage = InMemoryStorage()

    result = storage.delete_task("nonexistent-id")

    assert result is False


def test_get_task_count():
    """Test getting the task count."""
    storage = InMemoryStorage()

    assert storage.get_task_count() == 0

    task = Task(
        id="test-id",
        description="Test description",
        status="incomplete",
        created_date=datetime.now()
    )
    storage.add_task(task)

    assert storage.get_task_count() == 1

    storage.delete_task("test-id")

    assert storage.get_task_count() == 0


def test_clear_all():
    """Test clearing all tasks."""
    storage = InMemoryStorage()

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

    assert storage.get_task_count() == 2

    storage.clear_all()

    assert storage.get_task_count() == 0
    assert storage.get_task("test-id-1") is None
    assert storage.get_task("test-id-2") is None


def test_performance_stats():
    """Test that performance statistics are collected."""
    storage = InMemoryStorage()

    # Perform some operations
    task = Task(
        id="test-id",
        description="Test description",
        status="incomplete",
        created_date=datetime.now()
    )

    storage.add_task(task)
    storage.get_task("test-id")
    storage.update_task("test-id", task)
    storage.delete_task("test-id")

    stats = storage.get_performance_stats()

    # Check that stats were recorded
    assert stats['add_task_calls'] >= 1
    assert stats['get_task_calls'] >= 1
    assert stats['update_task_calls'] >= 1
    assert stats['delete_task_calls'] >= 1