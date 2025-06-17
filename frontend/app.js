const API_URL = "http://127.0.0.1:8000";
let currentUsername = localStorage.getItem('username') || '';

// Check if user is already set on page load
window.onload = function() {
    if (currentUsername) {
        showTaskSection();
        fetchTasks();
    }
};

function setUsername() {
    const usernameInput = document.getElementById('usernameInput');
    const username = usernameInput.value.trim();
    
    if (!username) {
        alert("Please enter a username!");
        return;
    }
    
    if (username.length < 3) {
        alert("Username must be at least 3 characters long!");
        return;
    }
    
    currentUsername = username;
    localStorage.setItem('username', username);
    showTaskSection();
    fetchTasks();
}

function showTaskSection() {
    document.querySelector('.username-section').style.display = 'none';
    document.getElementById('taskSection').style.display = 'block';
    document.getElementById('currentUser').textContent = currentUsername;
}

function changeUser() {
    currentUsername = '';
    localStorage.removeItem('username');
    document.querySelector('.username-section').style.display = 'block';
    document.getElementById('taskSection').style.display = 'none';
    document.getElementById('usernameInput').value = '';
    document.getElementById('taskInput').value = '';
    document.getElementById('taskList').innerHTML = '';
}

function fetchTasks() {
    if (!currentUsername) return;
    
    fetch(`${API_URL}/tasks/${currentUsername}`)
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
        })
        .catch(error => {
            console.error('Error fetching tasks:', error);
        });
}

function addTask() {
    if (!currentUsername) {
        alert("Please set a username first!");
        return;
    }
    
    const input = document.getElementById('taskInput');
    const title = input.value.trim();
    if (!title) {
        alert("Task title can't be empty.");
        return;
    }
    
    fetch(`${API_URL}/tasks/${currentUsername}`, {
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
    }).catch(error => {
        console.error('Error adding task:', error);
        alert("Failed to add task. Please try again.");
    });
}

function markDone(idx) {
    if (!currentUsername) return;
    
    fetch(`${API_URL}/tasks/${currentUsername}/${idx}`, {method: 'PUT'})
        .then(() => fetchTasks())
        .catch(error => {
            console.error('Error marking task done:', error);
        });
}

function deleteTask(idx) {
    if (!currentUsername) return;
    
    fetch(`${API_URL}/tasks/${currentUsername}/${idx}`, {method: 'DELETE'})
        .then(() => fetchTasks())
        .catch(error => {
            console.error('Error deleting task:', error);
        });
} 