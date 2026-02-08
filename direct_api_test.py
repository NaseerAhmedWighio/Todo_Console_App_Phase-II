#!/usr/bin/env python3
"""
Direct API test to see what's happening with the 72-byte error.
"""

import requests
import json
import hashlib


def test_direct_api_call():
    """Test the API directly with detailed debugging"""
    print("Testing direct API call...")
    print("=" * 50)

    # Test registration endpoint directly
    url = "http://localhost:8000/api/v1/auth/register"

    # Test with a long password
    test_data = {
        "email": "test@example.com",
        "password": "a" * 100,  # 100 characters
        "name": "Test User"
    }

    print(f"Sending registration request with password length: {len(test_data['password'])} characters")
    print(f"Password byte length: {len(test_data['password'].encode('utf-8'))} bytes")
    print(f"Request data: {json.dumps(test_data, indent=2)[:200]}...")

    try:
        response = requests.post(
            url,
            json=test_data,
            headers={"Content-Type": "application/json"}
        )

        print(f"Response Status Code: {response.status_code}")
        print(f"Response Body: {response.text}")

        if response.status_code >= 400:
            print("ERROR: Request failed!")
            # Let's also try with a shorter password to compare
            print("\nTrying with shorter password...")
            test_data_short = {
                "email": "test2@example.com",
                "password": "shortpass123",  # Short password
                "name": "Test User 2"
            }

            response2 = requests.post(
                url,
                json=test_data_short,
                headers={"Content-Type": "application/json"}
            )

            print(f"Short password response: {response2.status_code} - {response2.text}")

    except requests.exceptions.ConnectionError:
        print("ERROR: Cannot connect to backend server")
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

def test_fastapi_validation():
    """Test what happens when we call the FastAPI function directly"""
    print("\nTesting FastAPI validation...")
    print("=" * 50)

    # Import FastAPI components to test validation
    try:
        from backend.schemas.user import UserCreate

        # Test with long password
        print("Testing schema validation with long password...")
        try:
            user_data = UserCreate(
                email="test@example.com",
                password="a" * 100,
                name="Test User"
            )
            print(f"[SUCCESS] Schema validation passed. Password length: {len(user_data.password)}")
        except Exception as e:
            print(f"[ERROR] Schema validation failed: {e}")
            import traceback
            traceback.print_exc()

        # Test with problematic password
        print("\nTesting with known problematic password...")
        try:
            # This might be the exact error from bcrypt
            user_data = UserCreate(
                email="test@example.com",
                password="password cannot be longer than 72 bytes, truncate manually if necessary (e.g. my_password[:72])",
                name="Test User"
            )
            print(f"[SUCCESS] Schema validation passed. Password length: {len(user_data.password)}")
        except Exception as e:
            print(f"[ERROR] Schema validation failed: {e}")
            import traceback
            traceback.print_exc()

    except Exception as e:
        print(f"Error testing FastAPI validation: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("Direct API Test")
    print("=" * 60)

    test_direct_api_call()
    test_fastapi_validation()

    print("=" * 60)
    print("Direct API test completed!")