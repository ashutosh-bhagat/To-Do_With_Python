from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import get_db, User, Task, create_tables
from pydantic import BaseModel
from typing import List
import time
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

# Helper functions with better error handling
def get_or_create_user(db: Session, username: str) -> User:
    """Get existing user or create new one"""
    try:
        user = db.query(User).filter(User.username == username).first()
        if not user:
            user = User(username=username)
            db.add(user)
            db.commit()
            db.refresh(user)
        return user
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating/getting user {username}: {e}")
        raise HTTPException(status_code=500, detail="Database error")

def get_task_or_404(db: Session, username: str, task_id: int) -> Task:
    """Get task by ID for specific user or raise 404"""
    try:
        user = db.query(User).filter(User.username == username).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        task = db.query(Task).filter(Task.id == task_id, Task.user_id == user.id).first()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        return task
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting task {task_id} for user {username}: {e}")
        raise HTTPException(status_code=500, detail="Database error")

# API Endpoints with better error handling
@app.get("/tasks/{username}", response_model=List[TaskResponse])
def get_tasks(username: str, db: Session = Depends(get_db)):
    """Get all tasks for a specific user"""
    try:
        user = db.query(User).filter(User.username == username).first()
        if not user:
            return []  # Return empty list for new users
        
        tasks = db.query(Task).filter(Task.user_id == user.id).all()
        return tasks
    except Exception as e:
        logger.error(f"Error getting tasks for user {username}: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch tasks")

@app.post("/tasks/{username}", response_model=TaskResponse)
def add_task(username: str, task_data: TaskCreate, db: Session = Depends(get_db)):
    """Add a new task for a specific user"""
    try:
        title = task_data.title.strip()
        if not title:
            raise HTTPException(status_code=400, detail="Title required")
        
        user = get_or_create_user(db, username)
        
        new_task = Task(title=title, user_id=user.id)
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        
        return new_task
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error adding task for user {username}: {e}")
        raise HTTPException(status_code=500, detail="Failed to add task")

@app.put("/tasks/{username}/{task_id}", response_model=TaskResponse)
def mark_done(username: str, task_id: int, db: Session = Depends(get_db)):
    """Mark a task as done"""
    try:
        task = get_task_or_404(db, username, task_id)
        task.done = True
        db.commit()
        db.refresh(task)
        return task
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error marking task {task_id} done for user {username}: {e}")
        raise HTTPException(status_code=500, detail="Failed to update task")

@app.delete("/tasks/{username}/{task_id}")
def delete_task(username: str, task_id: int, db: Session = Depends(get_db)):
    """Delete a task"""
    try:
        task = get_task_or_404(db, username, task_id)
        db.delete(task)
        db.commit()
        return {"message": "Task deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting task {task_id} for user {username}: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete task")

# Health check endpoint
@app.get("/")
def read_root():
    return {"message": "Task Manager API is running!", "status": "healthy"}
