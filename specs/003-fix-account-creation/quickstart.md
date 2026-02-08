# Quickstart Guide: Fix Account Creation and Login Issues

## Overview
This guide provides essential information for developers implementing fixes for the 72-byte error and authentication issues in the Todo App.

## Prerequisites
- Node.js (v16 or higher)
- Python (v3.9 or higher)
- pip and npm/yarn
- Git

## Setup Instructions

### Backend Setup
```bash
cd backend
pip install -r requirements.txt  # or use uv/pip-tools as configured
python init_db.py
```

### Frontend Setup
```bash
cd frontend
npm install
```

## Configuration

### Environment Variables
Ensure the following environment variables are properly configured:

#### Backend (.env)
```env
BETTER_AUTH_SECRET=your-shared-secret-here
DATABASE_URL=sqlite:///./todo_app.db
SECRET_KEY=your-jwt-secret
```

#### Frontend (.env.local)
```env
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
BETTER_AUTH_SECRET=your-shared-secret-here
```

**Important**: The `BETTER_AUTH_SECRET` must be identical in both frontend and backend configurations.

## Running the Applications

### Backend
```bash
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend
```bash
cd frontend
npm run dev
```

## Key Implementation Areas

### Password Handling
- Location: `backend/core/jwt.py`
- Function: `get_password_hash()`
- Fix: Proper handling of bcrypt's 72-byte limitation
- Ensure passwords longer than 72 bytes are handled gracefully

### Authentication Integration
- Frontend: `frontend/lib/auth.ts`
- Backend: `backend/api/v1/auth.py`
- Ensure Better Auth and backend JWT validation are properly synchronized

### Error Handling
- Improve error messages to be user-friendly
- Log technical details for debugging without exposing them to users
- Handle edge cases for very long passwords

## Testing the Fix

### Manual Testing
1. Attempt to register with a password longer than 72 characters
2. Verify successful account creation
3. Log in with the same long password
4. Verify successful authentication

### API Testing
Use the following test scenarios:
```bash
# Register with long password
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "very_long_password_over_72_characters_here_with_various_symbols_and_numbers_to_test_the_limit", "name": "Test User"}'

# Login with long password
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "very_long_password_over_72_characters_here_with_various_symbols_and_numbers_to_test_the_limit"}'
```

## Troubleshooting

### Common Issues
1. **Different secrets between frontend and backend**: Ensure `BETTER_AUTH_SECRET` is identical
2. **Still seeing 72-byte errors**: Check that the password hashing function properly handles the limit
3. **Authentication failures**: Verify JWT validation configuration

### Debugging Tips
- Enable logging in auth endpoints to trace the flow
- Check that bcrypt library is properly configured
- Verify token generation and validation flow