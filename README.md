# To-Do_With_Python

<div align="center">

# To-Do App

*Empower your productivity, streamline your task management.*

<p>
  <img src="https://img.shields.io/github/last-commit/ashutosh-bhagat/WApp?color=blue&label=last%20commit&style=flat-square" alt="last commit">
  <img src="https://img.shields.io/badge/python-100%25-blue?style=flat-square" alt="python">
  <img src="https://img.shields.io/badge/languages-2-blue?style=flat-square" alt="languages">
</p>

**Built with the tools and technologies:**

<p>
  <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white" alt="HTML5">
  <img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white" alt="CSS3">
  <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" alt="JavaScript">
  <img src="https://img.shields.io/badge/JSON-000000?style=for-the-badge&logo=json&logoColor=white" alt="JSON">
  <img src="https://img.shields.io/badge/Markdown-000000?style=for-the-badge&logo=markdown&logoColor=white" alt="Markdown">
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
</p>

</div>

---

## Table of Contents

• [Overview](#overview)

• [Getting Started](#getting-started)

  • [Prerequisites](#prerequisites)
  
  • [Installation](#installation)

• [Usage](#usage)

• [Frontend](#frontend)

• [Testing](#testing)

• [Features](#features)

• [API Endpoints](#api-endpoints)

• [File Structure](#file-structure)

• [Contributing](#contributing)

---

## Overview

WApp is a powerful developer tool designed to streamline web application development through effective task management.

### Why WApp?

This project enhances collaboration and productivity by providing a structured approach to managing tasks. The core features include:

• 📋 **Structured Task Management**: Track project milestones and deliverables using a clear JSON format.

• 🎯 **User-Friendly Interface**: Manage tasks in real-time with an intuitive interface that boosts productivity. The frontend is now built with **HTML, CSS, and JavaScript** for a modern, responsive experience.

• ⚡ **High-Performance API**: Built on FastAPI, ensuring efficient handling of requests for seamless task operations.

• 🔧 **Modular Architecture**: Promotes ease of maintenance and integration, making it adaptable to various projects.

• 📦 **Efficient Task Organization**: Class-based structure allows for easy task creation, tracking, and exporting to JSON.

---

## Getting Started

### Prerequisites

This project requires the following dependencies:

• **Programming Language**: Python 3.8+
• **Package Manager**: Pip
• **Web Browser**: Chrome, Firefox, Edge, etc.

### Installation

Build WApp from the source and install dependencies:

1. **Clone the repository:**

```bash
git clone https://github.com/ashutosh-bhagat/WApp.git
```

2. **Navigate to the project directory:**

```bash
cd WApp
```

3. **Install the dependencies:**

Using **pip**:

```bash
pip install -r requirements.txt frontend_requirements.txt
```

---

## Usage

Run the project with:

**Using pip:**

```bash
python main.py
```

**Alternative execution:**

```bash
python -m uvicorn main:app --reload
```

The FastAPI server will start at `http://localhost:8000`

### API Documentation

Once running, visit:
- **Interactive API Docs**: `http://localhost:8000/docs`
- **ReDoc Documentation**: `http://localhost:8000/redoc`

---

## Frontend

The frontend is built with **HTML, CSS, and JavaScript** and is located in the `frontend/` directory.

### How to use the frontend

1. Make sure your FastAPI backend is running at `http://localhost:8000`.
2. Open `frontend/index.html` in your web browser.
3. You can now add, view, mark as done, and delete tasks in a modern UI.

---

## Testing

WApp uses the **pytest** test framework. Run the test suite with:

**Using pip:**

```bash
pytest
```

**Run with verbose output:**

```bash
pytest -v
```

**Run specific test files:**

```bash
pytest tests/test_tasks.py
pytest tests/test_api.py
```

---

## Features

### 🚀 Core Functionality

- **Task Creation**: Create new tasks with titles, descriptions, priorities, and due dates
- **Task Management**: Update, delete, and organize tasks efficiently
- **JSON Storage**: Persistent task storage using structured JSON format
- **Real-time Updates**: Instant task status updates and modifications
- **Search & Filter**: Advanced task filtering by status, priority, and date
- **Export/Import**: Backup and restore task data in JSON format

### 📊 Task Organization

- **Priority Levels**: High, Medium, Low priority assignment
- **Status Tracking**: Todo, In Progress, Completed status management
- **Category Tags**: Organize tasks by project or category
- **Due Date Management**: Set and track task deadlines
- **Progress Monitoring**: Visual progress indicators and completion rates

---

## API Endpoints

### Task Management

```http
GET    /tasks              # Get all tasks
POST   /tasks              # Create a new task
GET    /tasks/{task_id}    # Get specific task
PUT    /tasks/{task_id}    # Update task
DELETE /tasks/{task_id}    # Delete task
```

### Task Operations

```http
POST   /tasks/{task_id}/complete    # Mark task as complete
POST   /tasks/{task_id}/start       # Start task (set to in progress)
GET    /tasks/search                # Search tasks
GET    /tasks/filter                # Filter tasks by criteria
```

### Data Management

```http
GET    /export             # Export all tasks to JSON
POST   /import             # Import tasks from JSON
GET    /stats              # Get task statistics
```

---

## File Structure

```
WApp/
├── main.py                 # FastAPI application entry point
├── frontend/               # HTML, CSS, JS frontend
│   ├── index.html
│   ├── style.css
│   └── app.js
├── tasks.json             # Task data storage
├── README.md              # Project documentation
├── requirements.txt       # Python dependencies
├── frontend_requirements.txt  # Frontend dependencies
├── tests/                 # Test files
│   ├── test_tasks.py
│   └── test_api.py
└── static/               # Static files (CSS, JS, images)
    ├── css/
    ├── js/
    └── images/
```

---

## Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# Application Settings
APP_NAME=WApp
DEBUG=True
HOST=localhost
PORT=8000

# Database Settings (if using database)
DATABASE_URL=sqlite:///./tasks.db

# API Settings
API_V1_STR=/api/v1
SECRET_KEY=your-secret-key-here
```

---

## Development

### Setting up Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements.txt
pip install pytest black flake8 mypy

# Run code formatting
black .
flake8 .

# Type checking
mypy main.py
```

### Running in Development Mode

```bash
# With auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# With debug mode
python main.py --debug
```

---

## Deployment

### Production Deployment

```bash
# Install production dependencies
pip install gunicorn

# Run with Gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Docker Deployment

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## Contributing

We welcome contributions to WApp! Please follow these guidelines:

### How to Contribute

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Commit your changes** (`git commit -m 'Add some amazing feature'`)
4. **Push to the branch** (`git push origin feature/amazing-feature`)
5. **Open a Pull Request**

### Development Guidelines

- Follow PEP 8 style guidelines
- Write tests for new features
- Update documentation for API changes
- Use meaningful commit messages

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Support

If you encounter any issues or have questions:

- **GitHub Issues**: [Create an issue](https://github.com/ashutosh-bhagat/WApp/issues)
- **Documentation**: Check the `/docs` endpoint when running the application
- **Email**: ashutosh.bhagat@example.com

---

## Acknowledgments

- **FastAPI** for the high-performance web framework
- **Python Community** for excellent libraries and tools
- **Contributors** who help improve this project

---

<div align="center">

**⭐ Star this repository if you find it helpful!**

[🐛 Report Bug](https://github.com/ashutosh-bhagat/WApp/issues) • [✨ Request Feature](https://github.com/ashutosh-bhagat/WApp/issues) • [📖 Documentation](https://github.com/ashutosh-bhagat/WApp/wiki)

</div>
