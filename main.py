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

tasks = []

class Task:
    def __init__(self, title):
        self.title = title
        self.done = False

def get_task_or_404(task_id: int):
    if 0 <= task_id < len(tasks):
        return tasks[task_id]
    raise HTTPException(status_code=404, detail="Task not found")

@app.get("/tasks")
def get_tasks():
    return [{"id": i, "title": t.title, "done": t.done} for i, t in enumerate(tasks)]

@app.post("/tasks")
def add_task(task: dict):
    title = task.get("title", "").strip()
    if not title:
        raise HTTPException(status_code=400, detail="Title required")
    new_task = Task(title)
    tasks.append(new_task)
    return {"id": len(tasks)-1, "title": new_task.title, "done": new_task.done}

@app.put("/tasks/{task_id}")
def mark_done(task_id: int):
    task = get_task_or_404(task_id)
    task.done = True
    return {"id": task_id, "title": task.title, "done": task.done}

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    task = get_task_or_404(task_id)
    tasks.pop(task_id)
    return {"message": "Deleted"}
