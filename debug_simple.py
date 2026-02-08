#!/usr/bin/env python3
"""
Simple debug script to understand the exact source of the 72-byte password error.
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

    # Test with a long password
    test_password = "a" * 100  # 100 characters
    print(f"Original password length: {len(test_password)} characters")
    print(f"Original password byte length: {len(test_password.encode('utf-8'))} bytes")
    print()

    # Test our function
    print("Testing our get_password_hash function...")
    try:
        result = get_password_hash(test_password)
        print("[SUCCESS] Our function succeeded")
    except Exception as e:
        print(f"[ERROR] Our function failed: {e}")
        import traceback
        traceback.print_exc()
    print()

def debug_raw_bcrypt():
    """Test raw bcrypt behavior"""
    print("Testing raw bcrypt behavior...")
    print("=" * 50)

    import bcrypt

    # Test with different length passwords
    test_passwords = [
        "short",
        "a" * 72,
        "a" * 73,
        "a" * 100,
    ]

    for pwd in test_passwords:
        print(f"Testing password with {len(pwd)} characters ({len(pwd.encode('utf-8'))} bytes)")
        try:
            hashed = bcrypt.hashpw(pwd.encode('utf-8'), bcrypt.gensalt())
            print(f"  [SUCCESS] Raw bcrypt worked")
        except Exception as e:
            print(f"  [ERROR] Raw bcrypt failed: {e}")
        print()

def debug_passlib():
    """Test passlib behavior"""
    print("Testing passlib behavior...")
    print("=" * 50)

    from passlib.context import CryptContext
    import bcrypt

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__ident="2b")

    # Test with different length passwords
    test_passwords = [
        "short",
        "a" * 72,
        "a" * 73,
        "a" * 100,
    ]

    for pwd in test_passwords:
        print(f"Testing password with {len(pwd)} characters ({len(pwd.encode('utf-8'))} bytes)")
        try:
            result = pwd_context.hash(pwd)
            print(f"  [SUCCESS] Passlib worked")
        except Exception as e:
            print(f"  [ERROR] Passlib failed: {e}")
        print()

if __name__ == "__main__":
    print("Simple Password Issue Debug Script")
    print("=" * 60)

    debug_raw_bcrypt()
    print()
    debug_passlib()
    print()
    debug_password_hashing()

    print("=" * 60)
    print("Debugging completed!")