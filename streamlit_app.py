import streamlit as st
import requests

API_URL = "https://wapp-dpy4.onrender.com"  # Your local FastAPI

st.title("📋 Live Manager - Task App")

# --- Task Input ---
st.header("Add New Task")
task_input = st.text_input("Task title")

if st.button("Add Task"):
    
    if task_input.strip() != "":
        response = requests.post(f"{API_URL}/tasks", json={"title": task_input})
        st.success("✅ Task added successfully!")
    
    else:
        st.warning("Task title can't be empty.")

# --- List Tasks ---
st.header("🧾 Your Tasks")

tasks = requests.get(f"{API_URL}/tasks").json()

for idx, task in enumerate(tasks):
    col1, col2, col3 = st.columns([6, 1, 1])
    with col1:
        status = "✅" if task["done"] else "❌"
        st.write(f"{status} {task['title']}")
    with col2:
        if not task["done"]:
            if st.button("Mark Done", key=f"done_{idx}"):
                requests.put(f"{API_URL}/tasks/{idx}")
                st.rerun()

    with col3:
        if st.button("🗑️", key=f"del_{idx}"):
            requests.delete(f"{API_URL}/tasks/{idx}")
            st.rerun()

