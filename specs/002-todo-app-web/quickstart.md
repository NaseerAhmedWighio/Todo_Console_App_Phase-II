# Quickstart Guide: Todo App Phase II

## Overview
This guide provides the essential information to set up, develop, and deploy the Todo App Phase II - a full-stack web application with authentication and premium UI/UX.

## Prerequisites

### System Requirements
- Node.js 18+ (for frontend development)
- Python 3.9+ (for backend development)
- uv package manager (for Python dependencies)
- npm (for frontend dependencies)
- Git

### External Services
- Neon account for PostgreSQL database
- Better Auth account (or self-hosted instance)

## Setting Up the Development Environment

### 1. Clone and Initialize the Repository
```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Backend Setup (Python/FastAPI)
```bash
# Navigate to backend directory
cd backend/

# Install Python dependencies using uv
uv sync

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration
```

### 3. Frontend Setup (Next.js)
```bash
# Navigate to frontend directory
cd frontend/

# Install npm dependencies
npm install

# Set up environment variables
cp .env.local.example .env.local
# Edit .env.local with your configuration
```

## Environment Configuration

### Backend Environment Variables
```bash
# Database configuration
DATABASE_URL="postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require"

# Authentication configuration
BETTER_AUTH_SECRET="your-jwt-secret-key"
BETTER_AUTH_URL="http://localhost:3000"  # Your frontend URL

# Application settings
API_HOST="0.0.0.0"
API_PORT=8000
DEBUG=False
```

### Frontend Environment Variables
```bash
# Backend API configuration
NEXT_PUBLIC_API_BASE_URL="http://localhost:8000"
NEXT_PUBLIC_BETTER_AUTH_URL="http://localhost:3000"

# Authentication configuration
BETTER_AUTH_SECRET="same-secret-as-backend"
```

## Running the Applications

### 1. Start the Backend (FastAPI)
```bash
# From the backend directory
cd backend/
uv run python main.py
# Or using uvicorn directly
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Start the Frontend (Next.js)
```bash
# From the frontend directory
cd frontend/
npm run dev
```

### 3. Access the Application
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Backend API Documentation: http://localhost:8000/docs

## Key Development Commands

### Backend Commands
```bash
# Run tests
uv run pytest

# Run with auto-reload for development
uv run uvicorn main:app --reload

# Format code
uv run black .
uv run ruff check . --fix

# Generate database migrations
uv run alembic revision --autogenerate -m "migration message"
uv run alembic upgrade head
```

### Frontend Commands
```bash
# Development server
npm run dev

# Build for production
npm run build

# Run tests
npm run test

# Run linter
npm run lint

# Format code
npm run format
```

## Architecture Overview

### Backend Structure
```
backend/
├── main.py                 # Application entry point
├── models/                 # SQLModel database models
├── schemas/                # Pydantic request/response schemas
├── database/               # Database connection and session management
├── api/                    # API route definitions
│   └── v1/                 # API version 1 routes
│       ├── auth.py         # Authentication endpoints
│       └── tasks.py        # Task management endpoints
├── core/                   # Core application configuration
├── utils/                  # Utility functions
└── tests/                  # Test files
```

### Frontend Structure
```
frontend/
├── app/                    # Next.js App Router pages
│   ├── (auth)/             # Authentication-related pages
│   ├── (main)/             # Main application pages
│   │   ├── dashboard/      # Dashboard page
│   │   ├── tasks/          # Task management pages
│   │   └── profile/        # User profile page
│   ├── globals.css         # Global styles
│   ├── layout.tsx          # Root layout
│   └── page.tsx            # Homepage
├── components/             # Reusable React components
├── lib/                    # Utility functions and API clients
└── types/                  # TypeScript type definitions
```

## API Endpoints

### Authentication Endpoints
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration
- `POST /api/auth/logout` - User logout

### Task Management Endpoints
- `GET /api/{user_id}/tasks` - Get all user tasks
- `POST /api/{user_id}/tasks` - Create a new task
- `GET /api/{user_id}/tasks/{id}` - Get a specific task
- `PUT /api/{user_id}/tasks/{id}` - Update a task
- `DELETE /api/{user_id}/tasks/{id}` - Delete a task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle task completion

## Database Migrations

### Creating Migrations
```bash
cd backend/
uv run alembic revision --autogenerate -m "description of changes"
```

### Applying Migrations
```bash
cd backend/
uv run alembic upgrade head
```

### Downgrade Migrations
```bash
uv run alembic downgrade -1  # Go back one migration
uv run alembic downgrade base  # Revert all migrations
```

## Testing

### Backend Testing
```bash
# Run all tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=.

# Run specific test file
uv run pytest tests/test_tasks.py
```

### Frontend Testing
```bash
# Run all tests
npm run test

# Run tests in watch mode
npm run test:watch

# Run tests with coverage
npm run test:coverage
```

## Deployment

### Backend Deployment
1. Ensure environment variables are set appropriately
2. Run database migrations
3. Start the application server

### Frontend Deployment
1. Build the application: `npm run build`
2. Serve the built application using your preferred hosting solution

## Troubleshooting

### Common Issues
1. **Port conflicts**: Ensure ports 3000 (frontend) and 8000 (backend) are available
2. **Environment variables**: Verify all required environment variables are set
3. **Database connection**: Check that your Neon PostgreSQL connection string is correct
4. **Authentication**: Ensure BETTER_AUTH_SECRET matches between frontend and backend

### Development Tips
- Use `--reload` flag with uvicorn for auto-reload during development
- Check API documentation at `/docs` endpoint for FastAPI
- Use browser developer tools to inspect network requests and authentication headers