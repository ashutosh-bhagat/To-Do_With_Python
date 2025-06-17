from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, set this to your frontend's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store tasks per user: {username: [tasks]}
user_tasks = {}

class Task:
    def __init__(self, title):
        self.title = title
        self.done = False

def get_user_tasks(username: str):
    """Get or create task list for a user"""
    if username not in user_tasks:
        user_tasks[username] = []
    return user_tasks[username]

def get_task_or_404(username: str, task_id: int):
    tasks = get_user_tasks(username)
    if 0 <= task_id < len(tasks):
        return tasks[task_id]
    raise HTTPException(status_code=404, detail="Task not found")

@app.get("/tasks/{username}")
def get_tasks(username: str):
    tasks = get_user_tasks(username)
    return [{"id": i, "title": t.title, "done": t.done} for i, t in enumerate(tasks)]

@app.post("/tasks/{username}")
def add_task(username: str, task: dict):
    title = task.get("title", "").strip()
    if not title:
        raise HTTPException(status_code=400, detail="Title required")
    tasks = get_user_tasks(username)
    new_task = Task(title)
    tasks.append(new_task)
    return {"id": len(tasks)-1, "title": new_task.title, "done": new_task.done}

@app.put("/tasks/{username}/{task_id}")
def mark_done(username: str, task_id: int):
    task = get_task_or_404(username, task_id)
    task.done = True
    return {"id": task_id, "title": task.title, "done": task.done}

@app.delete("/tasks/{username}/{task_id}")
def delete_task(username: str, task_id: int):
    task = get_task_or_404(username, task_id)
    tasks = get_user_tasks(username)
    tasks.pop(task_id)
    return {"message": "Deleted"}
