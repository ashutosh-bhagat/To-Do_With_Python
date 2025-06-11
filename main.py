from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Task
from fastapi.middleware.cors import CORSMiddleware
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, set only your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logged_in_users = set()

@app.post("/signup")
def signup(user: dict):
    username = user.get("username")
    password = user.get("password")

    if not username or not password:
        raise HTTPException(status_code=400, detail="Username and password required")

    success = create_user(username, password)
    if not success:
        raise HTTPException(status_code=400, detail="User already exists")

    return {"message": "User created successfully"}


@app.post("/login")
def login(user: dict):
    username = user.get("username")
    password = user.get("password")

    if not verify_user(username, password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    logged_in_users.add(username)
    return {"message": "Login successful"}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/tasks")
def get_tasks(db: Session = Depends(get_db)):
    return db.query(Task).all()

@app.post("/tasks")
def add_task(task: dict, db: Session = Depends(get_db)):
    new_task = Task(title=task["title"])
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@app.put("/tasks/{task_id}")
def mark_done(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.done = True
    db.commit()
    return task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"message": "Deleted"}
