import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def create_task(title, description, priority="medium"):
    """Create a new task"""
    data = {
        "title": title,
        "description": description,
        "priority": priority
    }
    response = requests.post(f"{BASE_URL}/tasks/", json=data)
    print(f"Created task: {response.json()}")
    return response.json()

def get_tasks():
    """Get all tasks"""
    response = requests.get(f"{BASE_URL}/tasks/")
    print(f"Tasks: {json.dumps(response.json(), indent=2)}")
    return response.json()

def complete_task(task_id):
    """Mark task as completed"""
    response = requests.patch(f"{BASE_URL}/tasks/{task_id}/complete")
    print(f"Completed task: {response.json()}")
    return response.json()

if __name__ == "__main__":
    # Create some sample tasks
    task1 = create_task("Learn Python", "Master Python programming", "high")
    task2 = create_task("Setup Development Environment", "Install all necessary tools", "medium")
    task3 = create_task("Build API", "Create a RESTful API with FastAPI", "high")
    
    print("\n" + "="*50)
    print("ALL TASKS:")
    get_tasks()
    
    print("\n" + "="*50)
    print("COMPLETING FIRST TASK:")
    complete_task(task1["id"])
    
    print("\n" + "="*50)
    print("TASKS AFTER COMPLETION:")
    get_tasks()