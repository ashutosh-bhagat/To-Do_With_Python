const API_URL = "https://wapp-dpy4.onrender.com";

function fetchTasks() {
    fetch(`${API_URL}/tasks`)
        .then(res => res.json())
        .then(tasks => {
            const list = document.getElementById('taskList');
            list.innerHTML = '';
            tasks.forEach((task, idx) => {
                const li = document.createElement('li');
                li.innerHTML = `
                    <span class="status">${task.done ? '✅' : '❌'}</span>
                    <span class="${task.done ? 'done' : ''}">${task.title}</span>
                    <span>
                        ${!task.done ? `<button onclick="markDone(${idx})">Mark Done</button>` : ''}
                        <button onclick="deleteTask(${idx})">🗑️</button>
                    </span>
                `;
                list.appendChild(li);
            });
        });
}

function addTask() {
    const input = document.getElementById('taskInput');
    const title = input.value.trim();
    if (!title) {
        alert("Task title can't be empty.");
        return;
    }
    fetch(`${API_URL}/tasks`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({title})
    }).then(res => {
        if (res.ok) {
            input.value = '';
            fetchTasks();
        } else {
            res.json().then(data => alert(data.detail || "Something went wrong."));
        }
    });
}

function markDone(idx) {
    fetch(`${API_URL}/tasks/${idx}`, {method: 'PUT'})
        .then(() => fetchTasks());
}

function deleteTask(idx) {
    fetch(`${API_URL}/tasks/${idx}`, {method: 'DELETE'})
        .then(() => fetchTasks());
}

window.onload = fetchTasks; 