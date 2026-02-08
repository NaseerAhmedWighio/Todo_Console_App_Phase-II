# REST API Endpoints Specification

## Base URL
`/api/{user_id}/` where `{user_id}` is the authenticated user's ID from JWT token.

## Authentication Requirements
All endpoints require JWT authentication via `Authorization: Bearer <token>` header.
- 401 Unauthorized if no token or invalid token
- 403 Forbidden if token valid but user_id mismatch

## Endpoint Specifications

### Task Management Endpoints

#### GET /api/{user_id}/tasks
- **Purpose**: Retrieve all tasks for the authenticated user
- **Method**: GET
- **Path Params**: `{user_id}` - authenticated user's ID
- **Query Params**:
  - `completed=[true|false]` (optional) - filter by completion status
  - `limit={number}` (optional) - limit results
  - `offset={number}` (optional) - pagination offset
- **Headers**:
  - `Authorization: Bearer <jwt_token>`
- **Response Codes**:
  - 200 OK - Successful retrieval
  - 401 Unauthorized - Missing/invalid token
  - 403 Forbidden - User ID mismatch
- **Response Body**:
  ```json
  [
    {
      "id": 1,
      "user_id": "user_abc123",
      "title": "Sample task",
      "description": "Task description",
      "completed": false,
      "created_at": "2026-01-23T10:00:00Z",
      "updated_at": "2026-01-23T10:00:00Z"
    }
  ]
  ```

#### POST /api/{user_id}/tasks
- **Purpose**: Create a new task for the authenticated user
- **Method**: POST
- **Path Params**: `{user_id}` - authenticated user's ID
- **Headers**:
  - `Authorization: Bearer <jwt_token>`
  - `Content-Type: application/json`
- **Request Body**:
  ```json
  {
    "title": "New task title",
    "description": "Task description (optional)",
    "completed": false
  }
  ```
- **Response Codes**:
  - 201 Created - Task created successfully
  - 400 Bad Request - Invalid input data
  - 401 Unauthorized - Missing/invalid token
  - 403 Forbidden - User ID mismatch
- **Response Body**:
  ```json
  {
    "id": 1,
    "user_id": "user_abc123",
    "title": "New task title",
    "description": "Task description (optional)",
    "completed": false,
    "created_at": "2026-01-23T10:00:00Z",
    "updated_at": "2026-01-23T10:00:00Z"
  }
  ```

#### GET /api/{user_id}/tasks/{id}
- **Purpose**: Retrieve a specific task by ID for the authenticated user
- **Method**: GET
- **Path Params**:
  - `{user_id}` - authenticated user's ID
  - `{id}` - task ID
- **Headers**:
  - `Authorization: Bearer <jwt_token>`
- **Response Codes**:
  - 200 OK - Task found
  - 401 Unauthorized - Missing/invalid token
  - 403 Forbidden - User ID or task ownership mismatch
  - 404 Not Found - Task doesn't exist
- **Response Body**:
  ```json
  {
    "id": 1,
    "user_id": "user_abc123",
    "title": "Sample task",
    "description": "Task description",
    "completed": false,
    "created_at": "2026-01-23T10:00:00Z",
    "updated_at": "2026-01-23T10:00:00Z"
  }
  ```

#### PUT /api/{user_id}/tasks/{id}
- **Purpose**: Update an existing task for the authenticated user
- **Method**: PUT
- **Path Params**:
  - `{user_id}` - authenticated user's ID
  - `{id}` - task ID
- **Headers**:
  - `Authorization: Bearer <jwt_token>`
  - `Content-Type: application/json`
- **Request Body**:
  ```json
  {
    "title": "Updated task title",
    "description": "Updated task description",
    "completed": true
  }
  ```
- **Response Codes**:
  - 200 OK - Task updated successfully
  - 400 Bad Request - Invalid input data
  - 401 Unauthorized - Missing/invalid token
  - 403 Forbidden - User ID or task ownership mismatch
  - 404 Not Found - Task doesn't exist
- **Response Body**:
  ```json
  {
    "id": 1,
    "user_id": "user_abc123",
    "title": "Updated task title",
    "description": "Updated task description",
    "completed": true,
    "created_at": "2026-01-23T10:00:00Z",
    "updated_at": "2026-01-23T11:00:00Z"
  }
  ```

#### DELETE /api/{user_id}/tasks/{id}
- **Purpose**: Delete a specific task for the authenticated user
- **Method**: DELETE
- **Path Params**:
  - `{user_id}` - authenticated user's ID
  - `{id}` - task ID
- **Headers**:
  - `Authorization: Bearer <jwt_token>`
- **Response Codes**:
  - 204 No Content - Task deleted successfully
  - 401 Unauthorized - Missing/invalid token
  - 403 Forbidden - User ID or task ownership mismatch
  - 404 Not Found - Task doesn't exist
- **Response Body**: Empty

#### PATCH /api/{user_id}/tasks/{id}/complete
- **Purpose**: Toggle or set completion status of a task
- **Method**: PATCH
- **Path Params**:
  - `{user_id}` - authenticated user's ID
  - `{id}` - task ID
- **Headers**:
  - `Authorization: Bearer <jwt_token>`
  - `Content-Type: application/json`
- **Request Body**:
  ```json
  {
    "completed": true
  }
  ```
- **Response Codes**:
  - 200 OK - Task completion status updated
  - 400 Bad Request - Invalid input data
  - 401 Unauthorized - Missing/invalid token
  - 403 Forbidden - User ID or task ownership mismatch
  - 404 Not Found - Task doesn't exist
- **Response Body**:
  ```json
  {
    "id": 1,
    "user_id": "user_abc123",
    "title": "Sample task",
    "description": "Task description",
    "completed": true,
    "created_at": "2026-01-23T10:00:00Z",
    "updated_at": "2026-01-23T11:00:00Z"
  }
  ```

## Error Response Format
All error responses follow this format:
```json
{
  "detail": "Human-readable error message",
  "error_code": "machine-readable-error-code",
  "timestamp": "2026-01-23T10:00:00Z"
}
```

## Common Headers
- **Request Headers**:
  - `Authorization: Bearer <jwt_token>` - Required for all endpoints
  - `Content-Type: application/json` - For POST, PUT, PATCH requests
- **Response Headers**:
  - `Content-Type: application/json`
  - Standard CORS headers

## Rate Limiting
- Per-user rate limiting applied to prevent abuse
- Standard 429 Too Many Requests response when exceeded

## Validation
- All input data must be validated according to data model constraints
- Return 400 Bad Request with specific validation errors