#!/usr/bin/env python3
"""
Test script to verify the 72-byte password error fix implementation.
This script tests various password lengths to ensure the system handles them properly.
"""

import requests
import json
import time
import sys
import os

# Add the backend directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def test_password_hashing():
    """Test the password hashing function directly"""
    print("Testing password hashing function...")

    from backend.core.jwt import get_password_hash, verify_password

    # Test various password lengths
    test_passwords = [
        "short",  # Short password
        "a" * 50,  # Medium password
        "a" * 72,  # Exactly 72 bytes
        "a" * 73,  # Just over 72 bytes
        "a" * 100, # Longer password
        "a" * 128, # Maximum allowed password
        "hello world! This is a test password with unicode: ñáéíóú",  # Unicode password
    ]

    for i, password in enumerate(test_passwords):
        try:
            print(f"  Test {i+1}: Password length {len(password)} chars, {len(password.encode('utf-8'))} bytes")

            # Hash the password
            hashed = get_password_hash(password)
            print(f"    Hashed successfully")

            # Verify the password
            is_valid = verify_password(password, hashed)
            print(f"    Verification: {'PASS' if is_valid else 'FAIL'}")

            # Test with wrong password
            is_invalid = verify_password(password + "wrong", hashed)
            print(f"    Wrong password rejection: {'PASS' if not is_invalid else 'FAIL'}")

            print()
        except Exception as e:
            print(f"    ERROR: {str(e)}")
            print()


def test_api_endpoints():
    """Test the API endpoints for registration and login with long passwords"""
    print("Testing API endpoints...")

    base_url = "http://localhost:8000"

    # Test data with various password lengths
    test_cases = [
        {"password": "short123", "desc": "Short password"},
        {"password": "a" * 72, "desc": "Exactly 72 bytes"},
        {"password": "a" * 73, "desc": "Just over 72 bytes"},
        {"password": "a" * 100, "desc": "100 bytes password"},
        {"password": "a" * 128, "desc": "128 bytes password (max)"},
    ]

    for i, test_case in enumerate(test_cases):
        email = f"test{i}@example.com"
        password = test_case["password"]

        print(f"  Test {i+1}: {test_case['desc']} ({len(password)} chars, {len(password.encode('utf-8'))} bytes)")

        # Try to register
        try:
            register_response = requests.post(
                f"{base_url}/api/v1/auth/register",
                json={
                    "email": email,
                    "password": password,
                    "name": f"Test User {i+1}"
                },
                headers={"Content-Type": "application/json"}
            )

            if register_response.status_code in [200, 201]:
                print(f"    Registration: SUCCESS")

                # Try to login
                login_response = requests.post(
                    f"{base_url}/api/v1/auth/login",
                    json={
                        "email": email,
                        "password": password
                    },
                    headers={"Content-Type": "application/json"}
                )

                if login_response.status_code == 200:
                    print(f"    Login: SUCCESS")
                else:
                    print(f"    Login: FAILED - {login_response.status_code} {login_response.text}")
            else:
                print(f"    Registration: FAILED - {register_response.status_code} {register_response.text}")

        except requests.exceptions.ConnectionError:
            print(f"    SKIPPED - Backend not running at {base_url}")
            break
        except Exception as e:
            print(f"    ERROR: {str(e)}")

        print()


def main():
    """Main test function"""
    print("=" * 60)
    print("Testing 72-byte Password Error Fix Implementation")
    print("=" * 60)
    print()

    print("1. Testing password hashing function...")
    print("-" * 40)
    test_password_hashing()

    print("2. Testing API endpoints...")
    print("-" * 40)
    test_api_endpoints()

    print("=" * 60)
    print("Testing completed!")
    print("Check that:")
    print("- Passwords of various lengths (including >72 bytes) can be hashed")
    print("- Passwords of various lengths can be verified")
    print("- API registration and login work with long passwords")
    print("- No '72 bytes' errors occur")
    print("=" * 60)


if __name__ == "__main__":
    main()