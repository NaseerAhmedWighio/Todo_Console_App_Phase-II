# Backend Development Guidelines

## Technology Stack
- FastAPI (Python)
- SQLModel ORM
- Neon Serverless PostgreSQL

## Project Structure
```
backend/
├── main.py
├── models/
│   ├── __init__.py
│   ├── user.py
│   └── task.py
├── schemas/
│   ├── __init__.py
│   ├── user.py
│   └── task.py
├── database/
│   ├── __init__.py
│   └── session.py
├── api/
│   ├── __init__.py
│   ├── deps.py
│   └── v1/
│       ├── __init__.py
│       ├── auth.py
│       └── tasks.py
├── core/
│   ├── __init__.py
│   ├── config.py
│   ├── security.py
│   └── jwt.py
├── utils/
│   ├── __init__.py
│   └── helpers.py
└── tests/
    ├── __init__.py
    ├── conftest.py
    └── test_tasks.py
```

## Development Guidelines

### API Design
- Follow RESTful API conventions
- Use proper HTTP status codes
- Implement consistent response formats
- Document all endpoints with OpenAPI/Swagger

### Authentication & Authorization
- Implement JWT middleware for all protected routes
- Validate tokens using BETTER_AUTH_SECRET
- Extract user_id from JWT payload
- Enforce user data isolation at the API level
- Return 401 for invalid tokens, 403 for authorization failures

### Database Layer
- Use SQLModel for all database operations
- Define proper models with validation
- Implement proper indexing strategies
- Handle database connections with connection pooling
- Use async database operations where possible

### Error Handling
- Implement global exception handlers
- Return consistent error response format
- Log errors appropriately
- Never expose sensitive information in error messages

### Security
- Validate and sanitize all inputs
- Implement proper rate limiting
- Use parameterized queries to prevent SQL injection
- Protect against common vulnerabilities (XSS, CSRF, etc.)

### Testing
- Write comprehensive unit and integration tests
- Use pytest for testing framework
- Test all API endpoints and business logic
- Maintain 80%+ test coverage
- Test authentication and authorization flows

### Performance
- Implement proper database indexing
- Use async operations for I/O bound tasks
- Implement caching where appropriate
- Optimize database queries
- Monitor and optimize slow queries

### Configuration
- Use environment variables for configuration
- Implement proper secret management
- Configure connection pooling parameters
- Set up proper logging configuration

### Deployment
- Prepare for Neon PostgreSQL deployment
- Implement health check endpoints
- Configure proper monitoring and alerting
- Plan for scaling and load balancing