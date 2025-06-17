const API_URL = "http://127.0.0.1:8000"; // Changed to localhost for testing
let currentUsername = localStorage.getItem('username') || '';

// Check if user is already set on page load
window.onload = function() {
    if (currentUsername) {
        showTaskSection();
        fetchTasks();
    }
};

// Utility function for API calls with timeout and retry
async function apiCall(url, options = {}, retries = 2) {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 10000); // 10 second timeout
    
    console.log(`Making API call to: ${url}`, options); // Debug log
    
    try {
        const response = await fetch(url, {
            ...options,
            signal: controller.signal,
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            }
        });
        
        clearTimeout(timeoutId);
        
        console.log(`Response status: ${response.status}`); // Debug log
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        const data = await response.json();
        console.log(`Response data:`, data); // Debug log
        return data;
    } catch (error) {
        clearTimeout(timeoutId);
        
        if (error.name === 'AbortError') {
            throw new Error('Request timed out. Please try again.');
        }
        
        if (retries > 0) {
            console.log(`Retrying... ${retries} attempts left`);
            await new Promise(resolve => setTimeout(resolve, 1000)); // Wait 1 second before retry
            return apiCall(url, options, retries - 1);
        }
        
        throw error;
    }
}

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

async function fetchTasks() {
    if (!currentUsername) return;
    
    const list = document.getElementById('taskList');
    list.innerHTML = '<li class="loading">Loading tasks...</li>';
    
    try {
        const tasks = await apiCall(`${API_URL}/tasks/${currentUsername}`);
        
        list.innerHTML = '';
        if (tasks.length === 0) {
            list.innerHTML = '<li class="no-tasks">No tasks yet. Add your first task!</li>';
            return;
        }
        
        tasks.forEach((task, idx) => {
            const li = document.createElement('li');
            li.innerHTML = `
                <span class="status">${task.done ? '✅' : '❌'}</span>
                <span class="${task.done ? 'done' : ''}">${task.title}</span>
                <span class="task-actions">
                    ${!task.done ? `<button onclick="markDone(${task.id})" class="action-btn">Mark Done</button>` : ''}
                    <button onclick="deleteTask(${task.id})" class="action-btn delete-btn">🗑️</button>
                </span>
            `;
            list.appendChild(li);
        });
    } catch (error) {
        console.error('Error fetching tasks:', error);
        list.innerHTML = `<li class="error">Error loading tasks: ${error.message}</li>`;
    }
}

async function addTask() {
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
    
    // Show loading state
    const addButton = document.querySelector('button[onclick="addTask()"]');
    const originalText = addButton.textContent;
    addButton.textContent = 'Adding...';
    addButton.disabled = true;
    
    try {
        await apiCall(`${API_URL}/tasks/${currentUsername}`, {
            method: 'POST',
            body: JSON.stringify({title})
        });
        
        input.value = '';
        await fetchTasks();
    } catch (error) {
        console.error('Error adding task:', error);
        alert(`Failed to add task: ${error.message}`);
    } finally {
        addButton.textContent = originalText;
        addButton.disabled = false;
    }
}

async function markDone(taskId) {
    console.log(`Marking task ${taskId} as done`); // Debug log
    if (!currentUsername) return;
    
    try {
        await apiCall(`${API_URL}/tasks/${currentUsername}/${taskId}`, {
            method: 'PUT'
        });
        await fetchTasks();
    } catch (error) {
        console.error('Error marking task done:', error);
        alert(`Failed to mark task as done: ${error.message}`);
    }
}

async function deleteTask(taskId) {
    console.log(`Deleting task ${taskId}`); // Debug log
    if (!currentUsername) return;
    
    if (!confirm('Are you sure you want to delete this task?')) {
        return;
    }
    
    try {
        await apiCall(`${API_URL}/tasks/${currentUsername}/${taskId}`, {
            method: 'DELETE'
        });
        await fetchTasks();
    } catch (error) {
        console.error('Error deleting task:', error);
        alert(`Failed to delete task: ${error.message}`);
    }
} 