# Data Model: Todo App Phase II

## Overview
This document defines the data structures and relationships for the Todo App Phase II, focusing on the task management system with user isolation.

## Core Entities

### Task Entity
The primary entity representing a user's todo item.

**Fields**:
- `id` (Integer, Primary Key, Auto-generated): Unique identifier for the task
- `user_id` (String, Indexed): Identifier linking the task to its owner (matches Better Auth user ID)
- `title` (String, 1-255 characters, Required): The task title/description
- `description` (String, 0-1000 characters, Optional): Extended task details
- `completed` (Boolean, Default: false): Completion status of the task
- `created_at` (DateTime, Auto-generated): Timestamp when the task was created
- `updated_at` (DateTime, Auto-generated): Timestamp when the task was last modified

**Relationships**:
- Belongs to one User (via user_id foreign key reference to Better Auth user)

**Validation Rules**:
- Title must be 1-255 characters
- Description must be 0-1000 characters if provided
- user_id must match an authenticated user during creation/update
- Only the task owner can modify/delete the task

**State Transitions**:
- New Task: completed = false (default)
- Task Completed: completed = true
- Task Reopened: completed = false

### User Entity (Managed by Better Auth)
User accounts are managed by Better Auth, with the following relevant fields for our application:

**Fields**:
- `id` (String): Unique user identifier from Better Auth
- `email` (String): User's email address
- `name` (String): User's display name
- `created_at` (DateTime): Account creation timestamp

**Relationships**:
- Has many Tasks (via user_id foreign key in Task table)

## Database Schema

### Tasks Table
```sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for efficient querying
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_completed ON tasks(completed);
CREATE INDEX idx_tasks_user_completed ON tasks(user_id, completed);
```

## API Data Structures

### Task Creation Request
```json
{
  "title": "string (1-255 characters)",
  "description": "string (0-1000 characters, optional)",
  "completed": "boolean (default: false)"
}
```

### Task Response
```json
{
  "id": "integer",
  "user_id": "string",
  "title": "string",
  "description": "string or null",
  "completed": "boolean",
  "created_at": "ISO 8601 datetime string",
  "updated_at": "ISO 8601 datetime string"
}
```

### Task Update Request
```json
{
  "title": "string (1-255 characters)",
  "description": "string (0-1000 characters) or null",
  "completed": "boolean"
}
```

### Task Completion Toggle Request
```json
{
  "completed": "boolean"
}
```

## Data Access Patterns

### Query Patterns
1. **Get all tasks for a user**: Filter by user_id
2. **Get completed/incomplete tasks**: Filter by user_id and completed status
3. **Get specific task**: Filter by user_id and task id
4. **Count tasks**: Count by user_id with optional completion status filter

### Security Patterns
1. **User Isolation**: All queries must include user_id filter
2. **Ownership Validation**: Verify user_id in JWT matches user_id in record before operations
3. **Audit Trail**: Track creation and modification timestamps

## Validation Requirements

### At Database Level
- NOT NULL constraints on required fields
- Length constraints on string fields
- Default values for optional fields
- Foreign key constraints (where applicable)

### At Application Level
- User authentication validation
- User authorization validation (ownership check)
- Input sanitization
- Business rule validation

## Performance Considerations

### Indexing Strategy
- Primary index on id (auto-created)
- Index on user_id for efficient user-specific queries
- Index on completed for filtering by completion status
- Composite index on user_id and completed for combined filtering

### Partitioning Strategy
- Potential horizontal partitioning by user_id for large-scale deployments
- Time-based partitioning of historical data if needed

## Migration Considerations

### From Console App
- The existing console app uses SQLite with a different schema
- Migration would involve extracting user data and mapping to the new user-based model
- Need to establish user ownership for existing tasks (likely system-assigned user)

### Future Extensions
- Support for task categories/tags
- Support for task priorities
- Support for due dates and reminders
- Support for recurring tasks