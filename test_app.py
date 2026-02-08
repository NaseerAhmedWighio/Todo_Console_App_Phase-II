"""
Basic test script to verify that the todo application works correctly.
This tests the core functionality without requiring a full test suite.
"""
import sys
import os
import uuid
from datetime import datetime

# Add the project root to the Python path so imports work
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.models.task import Task, TaskCreate, TaskUpdate
from src.storage.in_memory import InMemoryStorage
from src.services.todo_service import TodoService


def test_basic_functionality():
    """Test the basic functionality of the todo application."""
    print("Testing basic functionality...")

    # Initialize storage and service
    storage = InMemoryStorage()
    service = TodoService(storage)

    # Test 1: Add a task
    print("\n1. Testing add_task functionality...")
    task_create = TaskCreate(description="Test task for verification")
    task = service.add_task(task_create)

    if task and task.description == "Test task for verification" and task.status == "incomplete":
        print("   ✓ Task created successfully with correct properties")
    else:
        print("   ✗ Task creation failed")
        return False

    # Test 2: Get all tasks
    print("\n2. Testing get_all_tasks functionality...")
    tasks = service.get_all_tasks()
    if len(tasks) == 1 and tasks[0].id == task.id:
        print("   ✓ Retrieved all tasks successfully")
    else:
        print("   ✗ Failed to retrieve all tasks")
        return False

    # Test 3: Get specific task
    print("\n3. Testing get_task functionality...")
    retrieved_task = service.get_task(task.id)
    if retrieved_task and retrieved_task.id == task.id:
        print("   ✓ Retrieved specific task successfully")
    else:
        print("   ✗ Failed to retrieve specific task")
        return False

    # Test 4: Update task
    print("\n4. Testing update_task functionality...")
    task_update = TaskUpdate(description="Updated test task")
    updated_task = service.update_task(task.id, task_update)

    if updated_task and updated_task.description == "Updated test task":
        print("   ✓ Task updated successfully")
    else:
        print("   ✗ Task update failed")
        return False

    # Test 5: Mark task as complete
    print("\n5. Testing mark_task_complete functionality...")
    completed_task = service.mark_task_complete(task.id)

    if completed_task and completed_task.status == "complete":
        print("   ✓ Task marked as complete successfully")
    else:
        print("   ✗ Failed to mark task as complete")
        return False

    # Test 6: Mark task as incomplete again
    print("\n6. Testing mark_task_incomplete functionality...")
    incomplete_task = service.mark_task_incomplete(task.id)

    if incomplete_task and incomplete_task.status == "incomplete":
        print("   ✓ Task marked as incomplete successfully")
    else:
        print("   ✗ Failed to mark task as incomplete")
        return False

    # Test 7: Delete task
    print("\n7. Testing delete_task functionality...")
    success = service.delete_task(task.id)

    if success:
        tasks_after_delete = service.get_all_tasks()
        if len(tasks_after_delete) == 0:
            print("   ✓ Task deleted successfully")
        else:
            print("   ✗ Task deletion failed - task still exists")
            return False
    else:
        print("   ✗ Task deletion failed")
        return False

    print("\n✓ All basic functionality tests passed!")
    return True


def test_edge_cases():
    """Test edge cases and error handling."""
    print("\n\nTesting edge cases...")

    # Initialize storage and service
    storage = InMemoryStorage()
    service = TodoService(storage)

    # Test 1: Try to get a non-existent task
    print("\n1. Testing retrieval of non-existent task...")
    fake_id = str(uuid.uuid4())
    retrieved_task = service.get_task(fake_id)

    if retrieved_task is None:
        print("   ✓ Correctly handled non-existent task")
    else:
        print("   ✗ Did not handle non-existent task properly")
        return False

    # Test 2: Try to update a non-existent task
    print("\n2. Testing update of non-existent task...")
    fake_id = str(uuid.uuid4())
    task_update = TaskUpdate(description="Should fail")
    updated_task = service.update_task(fake_id, task_update)

    if updated_task is None:
        print("   ✓ Correctly handled update of non-existent task")
    else:
        print("   ✗ Did not handle update of non-existent task properly")
        return False

    # Test 3: Try to delete a non-existent task
    print("\n3. Testing deletion of non-existent task...")
    fake_id = str(uuid.uuid4())
    success = service.delete_task(fake_id)

    if not success:
        print("   ✓ Correctly handled deletion of non-existent task")
    else:
        print("   ✗ Did not handle deletion of non-existent task properly")
        return False

    # Test 4: Try to mark complete a non-existent task
    print("\n4. Testing marking complete of non-existent task...")
    fake_id = str(uuid.uuid4())
    completed_task = service.mark_task_complete(fake_id)

    if completed_task is None:
        print("   ✓ Correctly handled marking complete of non-existent task")
    else:
        print("   ✗ Did not handle marking complete of non-existent task properly")
        return False

    # Test 5: Try to mark incomplete a non-existent task
    print("\n5. Testing marking incomplete of non-existent task...")
    fake_id = str(uuid.uuid4())
    incomplete_task = service.mark_task_incomplete(fake_id)

    if incomplete_task is None:
        print("   ✓ Correctly handled marking incomplete of non-existent task")
    else:
        print("   ✗ Did not handle marking incomplete of non-existent task properly")
        return False

    print("\n✓ All edge case tests passed!")
    return True


def test_validation():
    """Test validation functionality."""
    print("\n\nTesting validation...")

    # Initialize storage and service
    storage = InMemoryStorage()
    service = TodoService(storage)

    # Test 1: Try to create task with empty description
    print("\n1. Testing empty description validation...")
    try:
        # We'll test this by directly trying to create a Task object with empty description
        from pydantic import ValidationError
        try:
            invalid_task = Task(description="", status="incomplete")
            print("   ✗ Did not catch empty description validation")
            return False
        except ValidationError:
            print("   ✓ Correctly caught empty description validation")
    except ImportError:
        print("   ⚠ Skipping validation test - pydantic not available in this context")

    print("\n✓ Validation tests completed!")
    return True


def main():
    """Run all tests."""
    print("=" * 60)
    print("Todo Application - Basic Functionality Test")
    print("=" * 60)

    success = True

    success &= test_basic_functionality()
    success &= test_edge_cases()
    success &= test_validation()

    print("\n" + "=" * 60)
    if success:
        print("🎉 All tests passed! The todo application is working correctly.")
    else:
        print("❌ Some tests failed. Please check the implementation.")
    print("=" * 60)

    return success


if __name__ == "__main__":
    main()