#!/usr/bin/env python3
"""Debug script to test bcrypt hashing directly."""

from passlib.context import CryptContext

# Create the same context as in the application
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Test various passwords
test_passwords = [
    "simplepass123",
    "MBN.seer@456",
    "short",
    "a" * 70,  # Close to the limit
    "a" * 80,  # Over the limit
]

for pwd in test_passwords:
    print(f"Testing password: '{pwd}' (length: {len(pwd)})")
    try:
        hashed = pwd_context.hash(pwd)
        print(f"  Success: {hashed[:30]}...")
    except Exception as e:
        print(f"  Error: {e}")
    print()