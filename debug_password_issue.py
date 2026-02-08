#!/usr/bin/env python3
"""
Debug script to understand the exact source of the 72-byte password error.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def debug_password_hashing():
    """Debug the password hashing process step by step"""
    print("Debugging password hashing process...")
    print("=" * 50)

    # Import the required modules
    from backend.core.jwt import get_password_hash
    from passlib.context import CryptContext

    # Test with a long password
    test_password = "a" * 100  # 100 characters
    print(f"Original password length: {len(test_password)} characters")
    print(f"Original password byte length: {len(test_password.encode('utf-8'))} bytes")
    print(f"Password: {test_password[:20]}...{test_password[-10:]} (truncated for display)")
    print()

    # Test the raw bcrypt hashing
    print("Testing raw bcrypt hashing...")
    try:
        import bcrypt
        print(f"bcrypt version: {bcrypt.__version__}")

        # Test with the original password
        print("Trying to hash original password with bcrypt...")
        try:
            hashed = bcrypt.hashpw(test_password.encode('utf-8'), bcrypt.gensalt())
            print("✓ Raw bcrypt succeeded")
        except Exception as e:
            print(f"✗ Raw bcrypt failed: {e}")

        # Test with truncated password
        truncated = test_password[:72]
        print(f"Truncated to 72 chars, byte length: {len(truncated.encode('utf-8'))}")
        try:
            hashed = bcrypt.hashpw(truncated.encode('utf-8'), bcrypt.gensalt())
            print("✓ Raw bcrypt with truncated succeeded")
        except Exception as e:
            print(f"✗ Raw bcrypt with truncated failed: {e}")

    except ImportError:
        print("bcrypt module not available")
    print()

    # Test with passlib directly
    print("Testing with passlib CryptContext...")
    try:
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__ident="2b")

        # Test with original password
        print("Testing original password with passlib...")
        try:
            result = pwd_context.hash(test_password)
            print("✓ Passlib with original password succeeded")
        except Exception as e:
            print(f"✗ Passlib with original password failed: {e}")

        # Test with truncated password
        truncated = test_password[:72]
        print(f"Testing truncated password (72 chars) with passlib...")
        try:
            result = pwd_context.hash(truncated)
            print("✓ Passlib with truncated password succeeded")
        except Exception as e:
            print(f"✗ Passlib with truncated password failed: {e}")

    except Exception as e:
        print(f"Error testing passlib: {e}")
    print()

    # Test our function
    print("Testing our get_password_hash function...")
    try:
        result = get_password_hash(test_password)
        print("✓ Our function succeeded")
    except Exception as e:
        print(f"✗ Our function failed: {e}")
        import traceback
        traceback.print_exc()
    print()

def debug_full_flow():
    """Debug the full flow from schema validation to database"""
    print("Debugging full flow...")
    print("=" * 50)

    # Test schema validation
    print("Testing schema validation...")
    try:
        from backend.schemas.user import UserCreate

        # Create a user with a long password
        user_data = UserCreate(
            email="test@example.com",
            password="a" * 100,
            name="Test User"
        )
        print(f"✓ Schema validation passed - password length: {len(user_data.password)}")
    except Exception as e:
        print(f"✗ Schema validation failed: {e}")
    print()

    # Test service layer
    print("Testing service layer...")
    try:
        from backend.services.user_service import UserService
        from unittest.mock import MagicMock

        # Create mock session
        mock_session = MagicMock()
        user_data = UserCreate(
            email="test@example.com",
            password="a" * 100,
            name="Test User"
        )

        # Mock database operations
        import unittest.mock
        with unittest.mock.patch.object(mock_session, 'get', return_value=None):
            with unittest.mock.patch.object(mock_session, 'add'):
                with unittest.mock.patch.object(mock_session, 'commit'):
                    with unittest.mock.patch.object(mock_session, 'refresh'):
                        service = UserService(mock_session)

                        try:
                            result = service.create_user(user_data)
                            print("✓ Service layer succeeded")
                        except Exception as e:
                            print(f"✗ Service layer failed: {e}")
                            import traceback
                            traceback.print_exc()

    except Exception as e:
        print(f"✗ Error in service test setup: {e}")
    print()


if __name__ == "__main__":
    print("Password Issue Debug Script")
    print("=" * 60)

    debug_password_hashing()
    print()
    debug_full_flow()

    print("=" * 60)
    print("Debugging completed!")