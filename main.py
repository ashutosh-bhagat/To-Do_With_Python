from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Live Manager backend is live!"}



app = FastAPI()

# ------------------------
# Model for Request/Response
class Task(BaseModel):
    title: str
    done: bool = False

# ------------------------  
# In-memory Task List
tasks = []

# ------------------------
@app.get("/")
def home():
    return {"message": "Live Manager To-Do API"}

@app.get("/tasks")
def get_tasks():
    return tasks

@app.post("/tasks")
def create_task(task: Task):
    tasks.append(task)
    return {"message": "Task added successfully"}

@app.put("/tasks/{task_id}")
def mark_done(task_id: int):
    if task_id >= len(tasks) or task_id < 0:
        raise HTTPException(status_code=404, detail="Task not found")
    tasks[task_id].done = True
    return {"message": "Task marked as done"}

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    if task_id >= len(tasks) or task_id < 0:
        raise HTTPException(status_code=404, detail="Task not found")
    tasks.pop(task_id)
    return {"message": "Task deleted"}
