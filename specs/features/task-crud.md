# Task CRUD Operations Specification

## Feature Overview
Core task management functionality allowing users to create, read, update, delete, and complete tasks in a multi-user environment.

## Functional Requirements

### Create Task (POST)
- **Endpoint**: `/api/{user_id}/tasks`
- **Method**: POST
- **Authentication**: JWT required
- **Authorization**: User must match {user_id} in URL
- **Request Body**:
  ```json
  {
    "title": "string (required, max 255 chars)",
    "description": "string (optional, max 1000 chars)",
    "completed": "boolean (default: false)"
  }
  ```
- **Response**: 201 Created with task object
- **Validation**: Title required, proper length limits
- **Error Cases**: 400 (validation), 401 (auth), 403 (authz)

### Read All Tasks (GET)
- **Endpoint**: `/api/{user_id}/tasks`
- **Method**: GET
- **Authentication**: JWT required
- **Authorization**: User must match {user_id} in URL
- **Response**: 200 OK with array of task objects
- **Filtering**: Only return tasks belonging to authenticated user
- **Error Cases**: 401 (auth), 403 (authz)

### Read Single Task (GET)
- **Endpoint**: `/api/{user_id}/tasks/{id}`
- **Method**: GET
- **Authentication**: JWT required
- **Authorization**: User must match {user_id} in URL and own the task
- **Response**: 200 OK with task object or 404 if not found
- **Error Cases**: 401 (auth), 403 (authz), 404 (not found)

### Update Task (PUT)
- **Endpoint**: `/api/{user_id}/tasks/{id}`
- **Method**: PUT
- **Authentication**: JWT required
- **Authorization**: User must match {user_id} in URL and own the task
- **Request Body**: Same as create (all fields required)
- **Response**: 200 OK with updated task object
- **Validation**: All fields validated as in create
- **Error Cases**: 400 (validation), 401 (auth), 403 (authz), 404 (not found)

### Delete Task (DELETE)
- **Endpoint**: `/api/{user_id}/tasks/{id}`
- **Method**: DELETE
- **Authentication**: JWT required
- **Authorization**: User must match {user_id} in URL and own the task
- **Response**: 204 No Content
- **Error Cases**: 401 (auth), 403 (authz), 404 (not found)

### Toggle Complete Task (PATCH)
- **Endpoint**: `/api/{user_id}/tasks/{id}/complete`
- **Method**: PATCH
- **Authentication**: JWT required
- **Authorization**: User must match {user_id} in URL and own the task
- **Request Body**:
  ```json
  {
    "completed": "boolean"
  }
  ```
- **Response**: 200 OK with updated task object
- **Error Cases**: 400 (validation), 401 (auth), 403 (authz), 404 (not found)

## Data Model
```python
class Task(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: str  # Better Auth user ID
    title: str = Field(max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow})
```

## Business Rules
- Users can only access their own tasks
- Task titles must not be empty
- Description is optional
- Completion status can be toggled independently
- All timestamps are UTC

## Validation Rules
- Title: 1-255 characters
- Description: 0-1000 characters
- user_id: Must match authenticated user
- Task ID: Must exist and belong to user

## Error Handling
- 400: Bad Request (validation errors)
- 401: Unauthorized (missing/invalid JWT)
- 403: Forbidden (user mismatch)
- 404: Not Found (task doesn't exist)
- 500: Internal Server Error (unexpected issues)