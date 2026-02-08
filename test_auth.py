import requests
import json

# Base URL for the API
BASE_URL = "http://127.0.0.1:8000"

def test_registration():
    """Test user registration."""
    print("Testing user registration...")

    # Register a new user
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword123"
    }

    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=user_data)
        print(f"Registration response: {response.status_code}")
        print(f"Registration data: {response.json()}")

        if response.status_code == 201:
            print("✓ Registration successful")
            return True
        else:
            print(f"✗ Registration failed: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Registration error: {e}")
        return False

def test_login():
    """Test user login."""
    print("\nTesting user login...")

    # Login with the registered user
    login_data = {
        "username": "testuser",
        "password": "testpassword123"
    }

    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        print(f"Login response: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"Login data: {data}")
            print("✓ Login successful")
            return data.get("access_token")
        else:
            print(f"✗ Login failed: {response.text}")
            return None
    except Exception as e:
        print(f"✗ Login error: {e}")
        return None

def test_task_operations(token):
    """Test task operations with authentication."""
    print("\nTesting task operations...")

    headers = {"token": token}

    # Add a task
    task_data = {"description": "Test task from API"}
    try:
        response = requests.post(f"{BASE_URL}/tasks", json=task_data, headers=headers)
        print(f"Add task response: {response.status_code}")

        if response.status_code == 201:
            task = response.json()
            print(f"Added task: {task}")
            print("✓ Task added successfully")

            # Get the task ID for further operations
            task_id = task.get("id")
            return task_id
        else:
            print(f"✗ Task addition failed: {response.text}")
            return None
    except Exception as e:
        print(f"✗ Task addition error: {e}")
        return None

def test_logout(token):
    """Test user logout."""
    print("\nTesting user logout...")

    headers = {"token": token}

    try:
        response = requests.post(f"{BASE_URL}/auth/logout", headers=headers)
        print(f"Logout response: {response.status_code}")

        if response.status_code == 200:
            print("✓ Logout successful")
            return True
        else:
            print(f"✗ Logout failed: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Logout error: {e}")
        return False

if __name__ == "__main__":
    print("Testing the complete user authentication flow...\n")

    # Test registration
    if not test_registration():
        print("\n✗ Registration test failed")
        exit(1)

    # Test login
    token = test_login()
    if not token:
        print("\n✗ Login test failed")
        exit(1)

    # Test task operations
    task_id = test_task_operations(token)
    if not task_id:
        print("\n✗ Task operations test failed")
        exit(1)

    # Test logout
    if not test_logout(token):
        print("\n✗ Logout test failed")
        exit(1)

    print("\n✓ All tests passed! Authentication flow is working correctly.")