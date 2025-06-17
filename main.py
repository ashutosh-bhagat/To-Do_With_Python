from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import get_db, User, Task, create_tables
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Create tables on startup
create_tables()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, set this to your frontend's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response
class TaskCreate(BaseModel):
    title: str

class TaskResponse(BaseModel):
    id: int
    title: str
    done: bool
    
    class Config:
        from_attributes = True

# Helper functions
def get_or_create_user(db: Session, username: str) -> User:
    """Get existing user or create new one"""
    user = db.query(User).filter(User.username == username).first()
    if not user:
        user = User(username=username)
        db.add(user)
        db.commit()
        db.refresh(user)
    return user

def get_task_or_404(db: Session, username: str, task_id: int) -> Task:
    """Get task by ID for specific user or raise 404"""
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return task

# API Endpoints
@app.get("/tasks/{username}", response_model=List[TaskResponse])
def get_tasks(username: str, db: Session = Depends(get_db)):
    """Get all tasks for a specific user"""
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return []  # Return empty list for new users
    
    tasks = db.query(Task).filter(Task.user_id == user.id).all()
    return tasks

@app.post("/tasks/{username}", response_model=TaskResponse)
def add_task(username: str, task_data: TaskCreate, db: Session = Depends(get_db)):
    """Add a new task for a specific user"""
    title = task_data.title.strip()
    if not title:
        raise HTTPException(status_code=400, detail="Title required")
    
    user = get_or_create_user(db, username)
    
    new_task = Task(title=title, user_id=user.id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    
    return new_task

@app.put("/tasks/{username}/{task_id}", response_model=TaskResponse)
def mark_done(username: str, task_id: int, db: Session = Depends(get_db)):
    """Mark a task as done"""
    task = get_task_or_404(db, username, task_id)
    task.done = True
    db.commit()
    db.refresh(task)
    return task

@app.delete("/tasks/{username}/{task_id}")
def delete_task(username: str, task_id: int, db: Session = Depends(get_db)):
    """Delete a task"""
    task = get_task_or_404(db, username, task_id)
    db.delete(task)
    db.commit()
    return {"message": "Task deleted successfully"}

# Health check endpoint
@app.get("/")
def read_root():
    return {"message": "Task Manager API is running!"}
