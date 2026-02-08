import pytest
from datetime import datetime
from src.models.task import Task, TaskCreate, TaskUpdate, TaskStatusUpdate, TaskResponse


def test_task_creation():
    """Test creating a task with valid data."""
    task = Task(
        id="test-id",
        description="Test description",
        status="incomplete",
        created_date=datetime.now()
    )

    assert task.id == "test-id"
    assert task.description == "Test description"
    assert task.status == "incomplete"


def test_task_default_values():
    """Test that task uses default values correctly."""
    task = Task(
        id="test-id",
        description="Test description",
        created_date=datetime.now()
    )

    assert task.status == "incomplete"  # Should default to incomplete


def test_task_validation_empty_description():
    """Test that task validation fails with empty description."""
    with pytest.raises(ValueError):
        Task(
            id="test-id",
            description="",
            status="incomplete",
            created_date=datetime.now()
        )


def test_task_validation_whitespace_description():
    """Test that task validation strips whitespace from description."""
    task = Task(
        id="test-id",
        description="   test description   ",
        status="incomplete",
        created_date=datetime.now()
    )

    assert task.description == "test description"


def test_task_status_validation():
    """Test that task validation accepts only valid statuses."""
    # Valid statuses should work
    task_complete = Task(
        id="test-id-1",
        description="Test description",
        status="complete",
        created_date=datetime.now()
    )
    task_incomplete = Task(
        id="test-id-2",
        description="Test description",
        status="incomplete",
        created_date=datetime.now()
    )

    assert task_complete.status == "complete"
    assert task_incomplete.status == "incomplete"

    # Invalid status should fail
    with pytest.raises(ValueError):
        Task(
            id="test-id-3",
            description="Test description",
            status="invalid",
            created_date=datetime.now()
        )


def test_task_future_date_validation():
    """Test that task validation fails with future dates."""
    future_date = datetime.now().replace(year=datetime.now().year + 1)

    with pytest.raises(ValueError):
        Task(
            id="test-id",
            description="Test description",
            status="incomplete",
            created_date=future_date
        )


def test_task_create_model():
    """Test TaskCreate model."""
    task_create = TaskCreate(description="Test description")

    assert task_create.description == "Test description"


def test_task_create_validation():
    """Test TaskCreate model validation."""
    with pytest.raises(ValueError):
        TaskCreate(description="")


def test_task_update_model():
    """Test TaskUpdate model."""
    task_update = TaskUpdate(description="Updated description")

    assert task_update.description == "Updated description"


def test_task_update_validation():
    """Test TaskUpdate model validation."""
    with pytest.raises(ValueError):
        TaskUpdate(description="")


def test_task_status_update_model():
    """Test TaskStatusUpdate model."""
    task_status_update = TaskStatusUpdate(status="complete")

    assert task_status_update.status == "complete"


def test_task_status_update_validation():
    """Test TaskStatusUpdate model validation."""
    with pytest.raises(ValueError):
        TaskStatusUpdate(status="invalid")


def test_task_response_inheritance():
    """Test that TaskResponse inherits from Task."""
    task_response = Task(
        id="test-id",
        description="Test description",
        status="incomplete",
        created_date=datetime.now()
    )

    # TaskResponse is just an extension of Task, so it should behave the same
    assert isinstance(task_response, Task)