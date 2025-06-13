import streamlit as st
import requests

API_URL = "http://localhost:8000"  # Local FastAPI backend URL

st.title("📋 Live Manager - Task App")

# --- Add Task ---
st.subheader("Add New Task")
task_input = st.text_input("Task title")

if st.button("Add Task"):
    if task_input.strip() != "":
        response = requests.post(f"{API_URL}/tasks", json={"title": task_input})
        if response.status_code == 200:
            st.success("✅ Task added successfully!")
            st.rerun()
        else:
            st.error(response.json().get("detail", "Something went wrong."))
    else:
        st.warning("Task title can't be empty.")

# --- List Tasks ---
st.subheader("🧾 Your Tasks")
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
