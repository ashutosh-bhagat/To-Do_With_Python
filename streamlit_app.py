import streamlit as st
import requests

API_URL = "https://wapp-dpy4.onrender.com"  # Your FastAPI backend URL

# --- Session State ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""


st.title("📋 Live Manager - Task App")

# --- Auth Section ---
st.subheader("Login / Signup")

auth_mode = st.radio("Choose action:", ["Login", "Signup"], horizontal=True)
username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button(auth_mode):
    if not username or not password:
        st.warning("Please enter both username and password.")
    else:
        endpoint = f"{API_URL}/login" if auth_mode == "Login" else f"{API_URL}/signup"
        res = requests.post(endpoint, json={"username": username, "password": password})

        if res.status_code == 200:
            st.success(f"{auth_mode} successful!")
            st.session_state.logged_in = True
            st.session_state.username = username
            st.rerun()
        else:
            st.error(res.json().get("detail", "Something went wrong."))


# --- Main Task App ---
if st.session_state.logged_in:
    st.header(f"Welcome, {st.session_state.username}! 👋")

    # --- Add Task ---
    st.subheader("Add New Task")
    task_input = st.text_input("Task title")

    if st.button("Add Task"):
        if task_input.strip() != "":
            response = requests.post(f"{API_URL}/tasks", json={"title": task_input})
            st.success("✅ Task added successfully!")
            st.rerun()
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

else:
    st.info("Please log in to use the task manager.")
