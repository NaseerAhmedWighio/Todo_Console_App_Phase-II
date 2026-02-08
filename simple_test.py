#!/usr/bin/env python3
"""
Simple test to debug the 72-byte error issue
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def test_direct_import():
    """Test importing and using the functions directly"""
    print("Testing direct import and function calls...")

    from backend.core.jwt import get_password_hash, verify_password

    # Test a simple password
    password = "test_password_123"
    print(f"Testing with password: '{password}' (length: {len(password)})")

    try:
        hashed = get_password_hash(password)
        print(f"✓ Hashing successful: {type(hashed)}")

        # Verify
        is_valid = verify_password(password, hashed)
        print(f"✓ Verification: {is_valid}")

    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()

def test_long_password():
    """Test with a long password"""
    print("\nTesting with a long password...")

    from backend.core.jwt import get_password_hash, verify_password

    # Create a 100-character password
    password = "a" * 100
    print(f"Testing with password of length: {len(password)}")

    try:
        hashed = get_password_hash(password)
        print(f"✓ Hashing successful: {type(hashed)}")

        # Verify with the same password (should work after our fix)
        is_valid = verify_password(password, hashed)
        print(f"✓ Verification with original password: {is_valid}")

        # Verify with truncated version too
        truncated = password[:72]
        is_valid_truncated = verify_password(truncated, hashed)
        print(f"✓ Verification with truncated password: {is_valid_truncated}")

    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()

def test_user_service():
    """Test the user service directly"""
    print("\nTesting UserService directly...")

    # Create a mock session
    from unittest.mock import MagicMock
    mock_session = MagicMock()

    # Create user data
    from backend.schemas.user import UserCreate
    user_data = UserCreate(
        email="test@example.com",
        password="a" * 100,  # Long password
        name="Test User"
    )

    print(f"Created user data with password length: {len(user_data.password)}")

    try:
        from backend.services.user_service import UserService
        service = UserService(mock_session)

        # This should trigger the error
        # But we'll need to patch the database calls
        import unittest.mock

        with unittest.mock.patch.object(mock_session, 'get', return_value=None):
            with unittest.mock.patch.object(mock_session, 'add'):
                with unittest.mock.patch.object(mock_session, 'commit'):
                    with unittest.mock.patch.object(mock_session, 'refresh'):
                        # Mock the user object that gets returned
                        mock_user = MagicMock()
                        mock_user.id = "user_123"
                        mock_user.email = "test@example.com"
                        mock_user.name = "Test User"
                        mock_user.hashed_password = "mock_hash"

                        result = service.create_user(user_data)
                        print(f"✓ UserService.create_user worked: {result}")

    except Exception as e:
        print(f"✗ UserService error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("=" * 50)
    print("Simple Debug Test for 72-byte Error")
    print("=" * 50)

    test_direct_import()
    test_long_password()
    test_user_service()

    print("\n" + "=" * 50)
    print("Debug test completed!")
    print("=" * 50)