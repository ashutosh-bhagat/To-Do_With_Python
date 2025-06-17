import requests
import json

# Test the API endpoints
base_url = "http://127.0.0.1:8000"
username = "testuser"

def test_mark_done_and_delete():
    print("Testing mark done and delete functionality...")
    
    # 1. First, add a task
    print("\n1. Adding a test task...")
    task_data = {"title": "Test task for mark done"}
    response = requests.post(
        f"{base_url}/tasks/{username}",
        headers={"Content-Type": "application/json"},
        data=json.dumps(task_data)
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        task = response.json()
        task_id = task['id']
        print(f"Task created with ID: {task_id}")
        print(f"Task: {task}")
    else:
        print(f"Error: {response.text}")
        return
    
    # 2. Get all tasks to verify
    print("\n2. Getting all tasks...")
    response = requests.get(f"{base_url}/tasks/{username}")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        tasks = response.json()
        print(f"All tasks: {tasks}")
    else:
        print(f"Error: {response.text}")
        return
    
    # 3. Mark the task as done
    print(f"\n3. Marking task {task_id} as done...")
    response = requests.put(f"{base_url}/tasks/{username}/{task_id}")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        updated_task = response.json()
        print(f"Task marked as done: {updated_task}")
    else:
        print(f"Error: {response.text}")
        return
    
    # 4. Get all tasks again to verify the change
    print("\n4. Getting all tasks after marking done...")
    response = requests.get(f"{base_url}/tasks/{username}")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        tasks = response.json()
        print(f"All tasks after mark done: {tasks}")
    else:
        print(f"Error: {response.text}")
        return
    
    # 5. Delete the task
    print(f"\n5. Deleting task {task_id}...")
    response = requests.delete(f"{base_url}/tasks/{username}/{task_id}")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Delete result: {result}")
    else:
        print(f"Error: {response.text}")
        return
    
    # 6. Get all tasks one more time to verify deletion
    print("\n6. Getting all tasks after deletion...")
    response = requests.get(f"{base_url}/tasks/{username}")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        tasks = response.json()
        print(f"All tasks after deletion: {tasks}")
    else:
        print(f"Error: {response.text}")

if __name__ == "__main__":
    test_mark_done_and_delete() 