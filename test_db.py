import requests
import json

# Test the API endpoints
base_url = "http://127.0.0.1:8000"

def test_api():
    print("Testing Task Manager API...")
    
    # Test health endpoint
    print("\n1. Testing health endpoint:")
    response = requests.get(f"{base_url}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Test getting tasks for new user
    print("\n2. Testing get tasks for new user:")
    response = requests.get(f"{base_url}/tasks/testuser")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Test adding a task
    print("\n3. Testing add task:")
    task_data = {"title": "Test task from script"}
    try:
        response = requests.post(
            f"{base_url}/tasks/testuser",
            headers={"Content-Type": "application/json"},
            data=json.dumps(task_data)
        )
        print(f"Status: {response.status_code}")
        print(f"Response text: {response.text}")
        if response.status_code == 200:
            print(f"Response JSON: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test getting tasks again
    print("\n4. Testing get tasks after adding:")
    response = requests.get(f"{base_url}/tasks/testuser")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

if __name__ == "__main__":
    test_api() 