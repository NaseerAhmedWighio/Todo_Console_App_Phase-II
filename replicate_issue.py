#!/usr/bin/env python3
"""
Script to replicate the exact issue happening in the API.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def test_replicate_issue():
    """Replicate the exact issue from the API endpoint"""
    print("Replicating the issue...")
    print("=" * 50)

    # Simulate what happens in the auth endpoint
    from backend.schemas.user import UserCreate
    from backend.services.user_service import UserService
    from backend.database.session import engine
    from sqlmodel import Session

    # Create a session (like the API does)
    with Session(engine) as session:
        # Create user data like in the API
        user_data = UserCreate(
            email="test@example.com",
            password="a" * 100,  # Long password
            name="Test User"
        )

        print(f"Created user_data with email: {user_data.email}")
        print(f"Password length: {len(user_data.password)} characters")
        print(f"Password byte length: {len(user_data.password.encode('utf-8'))} bytes")

        # Create user service
        user_service = UserService(session)

        print("\nCalling user_service.create_user...")
        try:
            user = user_service.create_user(user_data)
            print(f"[SUCCESS] User created: {user}")
        except Exception as e:
            print(f"[ERROR] user_service.create_user failed: {e}")
            print(f"Error type: {type(e)}")
            import traceback
            traceback.print_exc()

    print("\n" + "=" * 50)

def test_database_connection():
    """Test the database connection"""
    print("Testing database connection...")
    print("=" * 50)

    from backend.database.session import engine
    from sqlmodel import Session
    from backend.models.user import User
    from sqlmodel import select

    try:
        with Session(engine) as session:
            # Try a simple query
            statement = select(User).limit(1)
            result = session.exec(statement)
            users = result.all()
            print(f"[SUCCESS] Database query worked. Found {len(users)} users")
    except Exception as e:
        print(f"[ERROR] Database connection failed: {e}")
        import traceback
        traceback.print_exc()

    print("\n" + "=" * 50)

if __name__ == "__main__":
    print("Replicating Issue Script")
    print("=" * 60)

    test_database_connection()
    test_replicate_issue()

    print("Replication test completed!")