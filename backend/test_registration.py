"""Test script to verify user registration works."""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from sqlmodel import create_engine, Session
from core.config import settings
from database.session import get_session
from models.user import User, UserRead
from schemas.user import UserCreate
from services.user_service import UserService
import uuid

# Create a test session
engine = create_engine(settings.database_url)
session = Session(engine)

try:
    # Create user service
    user_service = UserService(session)

    # Create test user data
    user_data = UserCreate(
        email="test.registration@example.com",
        password="testpassword123",
        name="Test User"
    )

    print("Attempting to create user...")
    created_user = user_service.create_user(user_data)
    print(f"User created successfully: {created_user}")
    print(f"User ID: {created_user.id}")
    print(f"User email: {created_user.email}")

    # Test authentication
    print("\nTesting authentication...")
    authenticated_user = user_service.authenticate_user("test.registration@example.com", "testpassword123")
    if authenticated_user:
        print(f"Authentication successful: {authenticated_user}")
    else:
        print("Authentication failed")

except Exception as e:
    print(f"Error during registration: {e}")
    import traceback
    traceback.print_exc()
finally:
    session.close()