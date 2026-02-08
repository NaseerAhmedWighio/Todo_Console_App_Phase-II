#!/usr/bin/env python3
"""Test script to verify Better Auth compatible endpoints are working"""

import requests
import json

def test_better_auth_endpoints():
    base_url = "http://localhost:8000"

    print("Testing Better Auth compatible endpoints...")

    # Test sign-up endpoint
    print("\n1. Testing sign-up endpoint...")
    try:
        signup_response = requests.post(
            f"{base_url}/api/auth/sign-up/email",
            json={
                "email": "test_better_auth@example.com",
                "password": "testpassword123",
                "name": "Test User"
            },
            headers={"Content-Type": "application/json"}
        )
        print(f"Sign-up status: {signup_response.status_code}")
        if signup_response.status_code == 200:
            print("✅ Sign-up endpoint working correctly")
            signup_data = signup_response.json()
            print(f"Response: {json.dumps(signup_data, indent=2)}")
        else:
            print(f"❌ Sign-up failed: {signup_response.text}")
    except Exception as e:
        print(f"❌ Sign-up test error: {e}")

    # Test sign-in endpoint
    print("\n2. Testing sign-in endpoint...")
    try:
        signin_response = requests.post(
            f"{base_url}/api/auth/sign-in/credentials",
            json={
                "email": "test_better_auth@example.com",
                "password": "testpassword123"
            },
            headers={"Content-Type": "application/json"}
        )
        print(f"Sign-in status: {signin_response.status_code}")
        if signin_response.status_code == 200:
            print("✅ Sign-in endpoint working correctly")
            signin_data = signin_response.json()
            print(f"Response: {json.dumps(signin_data, indent=2)}")
        else:
            print(f"❌ Sign-in failed: {signin_response.text}")
    except Exception as e:
        print(f"❌ Sign-in test error: {e}")

    # Test get-session endpoint
    print("\n3. Testing get-session endpoint...")
    try:
        # Need to get a token from sign-in first, or use a dummy request
        session_response = requests.post(
            f"{base_url}/api/auth/get-session",
            headers={"Content-Type": "application/json"}
        )
        print(f"Get-session status: {session_response.status_code}")
        print("✅ Get-session endpoint accessible")
        session_data = session_response.json()
        print(f"Response: {json.dumps(session_data, indent=2)}")
    except Exception as e:
        print(f"❌ Get-session test error: {e}")

    # Test sign-out endpoint
    print("\n4. Testing sign-out endpoint...")
    try:
        signout_response = requests.post(
            f"{base_url}/api/auth/sign-out",
            headers={"Content-Type": "application/json"}
        )
        print(f"Sign-out status: {signout_response.status_code}")
        if signout_response.status_code == 200:
            print("✅ Sign-out endpoint working correctly")
            signout_data = signout_response.json()
            print(f"Response: {json.dumps(signout_data, indent=2)}")
        else:
            print(f"❌ Sign-out failed: {signout_response.text}")
    except Exception as e:
        print(f"❌ Sign-out test error: {e}")

    print("\nBetter Auth integration test completed!")

if __name__ == "__main__":
    test_better_auth_endpoints()