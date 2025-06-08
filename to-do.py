import json

class Task:
    def __init__(self, title):
        self.title = title
        self.done = False

    def mark_done(self):
        self.done = True

class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, title):
        self.tasks.append(Task(title))

    def list_tasks(self):
        for i, task in enumerate(self.tasks, 1):
            status = "✅" if task.done else "❌"
            print(f"{i}. {task.title} [{status}]")

    def mark_done(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index].mark_done()
        else:
            print("Invalid task number.")

    def delete_task(self, index):
        if 0 <= index < len(self.tasks):
            del self.tasks[index]
        else:
            print("Invalid task number.")

    def export_tasks_to_json(self, filename="tasks.json"):
        data = []
        for task in self.tasks:
            data.append({
                "title": task.title,
                "done": task.done
            })
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
            # this json.dumb makes the thing human readable in the json file
        print(f"Tasks exported to {filename}")

# Demo
tm = TaskManager()
tm.add_task("Build class version")
tm.add_task("Design architecture")
tm.list_tasks()
tm.mark_done(1)
tm.list_tasks()
tm.add_task("The App is building....")
tm.add_task("Build the App")
tm.list_tasks()
tm.mark_done(3)
tm.list_tasks()
tm.export_tasks_to_json()
