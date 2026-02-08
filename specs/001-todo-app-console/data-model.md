# Data Model: In-Memory Python Console App Todo Application

## Task Entity

### Fields
- **id** (str): Unique identifier for the task, automatically generated using UUID
- **description** (str): Text content of the task, required field with min length of 1 character
- **status** (str): Current status of the task, either "incomplete" or "complete", defaults to "incomplete"
- **created_date** (datetime): Timestamp when the task was created, automatically set on creation

### Validation Rules
- Description must not be empty
- Status must be either "incomplete" or "complete"
- ID must be unique across all tasks
- Created date must be in the past or present

### State Transitions
- From "incomplete" to "complete": When user marks task as complete
- From "complete" to "incomplete": When user marks task as incomplete

## Task List Container

### Operations
- **add_task(description: str)**: Creates a new task with the provided description and adds it to the list with "incomplete" status
- **get_task(task_id: str)**: Retrieves a specific task by its ID
- **get_all_tasks()**: Returns all tasks in the list
- **update_task(task_id: str, description: str)**: Modifies the description of an existing task
- **delete_task(task_id: str)**: Removes a task from the list by its ID
- **mark_task_complete(task_id: str)**: Changes task status to "complete"
- **mark_task_incomplete(task_id: str)**: Changes task status to "incomplete"

### Constraints
- Maximum of 1000 tasks allowed in memory at one time
- Thread-safe operations to handle concurrent access
- Atomic operations to prevent race conditions