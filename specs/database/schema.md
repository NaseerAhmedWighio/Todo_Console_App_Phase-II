# Database Schema Specification

## Database System
- **Type**: PostgreSQL (Neon Serverless)
- **ORM**: SQLModel (SQLAlchemy + Pydantic)
- **Connection**: Connection pooling with proper error handling

## Tables

### Users Table (Managed by Better Auth)
The users table is managed by Better Auth and contains standard user account information:
- `id`: Primary identifier from Better Auth
- `email`: User's email address
- `name`: User's display name
- `image`: Profile picture URL (optional)
- `email_verified`: Boolean indicating email verification status
- `created_at`: Account creation timestamp
- `updated_at`: Last update timestamp

### Tasks Table
The tasks table stores all todo items with user ownership:

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
```

#### Columns Details:
- `id`: Auto-incrementing integer primary key
- `user_id`: Foreign key reference to Better Auth user ID (VARCHAR 255)
- `title`: Task title (VARCHAR 255, NOT NULL)
- `description`: Optional task description (TEXT)
- `completed`: Boolean indicating completion status (DEFAULT FALSE)
- `created_at`: Timestamp of record creation (TIMESTAMP WITH TIME ZONE)
- `updated_at`: Timestamp of last update (TIMESTAMP WITH TIME ZONE)

#### Indexes:
```sql
-- Index for efficient user-based queries
CREATE INDEX idx_tasks_user_id ON tasks(user_id);

-- Index for filtering completed tasks
CREATE INDEX idx_tasks_completed ON tasks(completed);

-- Composite index for user and completion status
CREATE INDEX idx_tasks_user_completed ON tasks(user_id, completed);

-- Index for sorting by creation date
CREATE INDEX idx_tasks_created_at ON tasks(created_at);
```

## SQLModel Definitions

### Task Model
```python
from sqlmodel import SQLModel, Field, create_engine
from typing import Optional
from datetime import datetime

class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = False

class Task(TaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow,
                                sa_column_kwargs={"onupdate": datetime.utcnow})

class TaskCreate(TaskBase):
    pass

class TaskRead(TaskBase):
    id: int
    user_id: str
    created_at: datetime
    updated_at: datetime

class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
```

## Relationships
- Each task belongs to exactly one user (many-to-one relationship)
- User identity is managed externally by Better Auth
- No direct foreign key constraint to users table (to avoid coupling with Better Auth schema)

## Constraints
- `title` cannot be empty (min_length=1)
- `title` has maximum length of 255 characters
- `description` has maximum length of 1000 characters
- `completed` defaults to FALSE
- All timestamps use UTC timezone

## Security Considerations
- No direct user table access - rely on Better Auth user IDs
- All queries must filter by user_id for data isolation
- Proper parameterized queries to prevent SQL injection
- Connection pooling with secure credentials

## Performance Considerations
- Proper indexing on user_id for efficient queries
- Index on completed status for filtering
- Efficient pagination support
- Connection pooling for high concurrency

## Migration Strategy
- Use Alembic for database migrations
- Support both forward and rollback operations
- Maintain backward compatibility during upgrades
- Backup procedures for schema changes

## Connection Pooling
- Configure appropriate pool sizes for application load
- Set connection timeouts to prevent hanging connections
- Implement retry logic for transient failures
- Monitor connection usage for optimization