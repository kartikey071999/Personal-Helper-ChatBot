import sqlite3

def add_task(description: str) -> str:
    """Adds a new task to the to-do list."""
    try:
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
        c.execute("INSERT INTO tasks (description) VALUES (?)", (description,))
        conn.commit()
        conn.close()
        return f"Successfully added task: '{description}'"
    except Exception as e:
        return f"Error adding task: {e}"

def complete_task(task_id: int) -> str:
    """Marks a task as 'done' based on its ID."""
    try:
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
        c.execute("UPDATE tasks SET status = 'done' WHERE id = ?", (task_id,))
        conn.commit()
        conn.close()
        return f"Successfully completed task {task_id}."
    except Exception as e:
        return f"Error completing task: {e}"

def list_tasks() -> str:
    """Lists all 'todo' tasks from the database."""
    try:
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
        c.execute("SELECT id, description FROM tasks WHERE status = 'todo'")
        tasks = c.fetchall()
        conn.close()
        
        if not tasks:
            return "Your to-do list is empty!"
        
        # Format the list for the AI
        task_list_str = "Your active tasks:\n"
        for task in tasks:
            task_list_str += f"- (ID: {task[0]}) {task[1]}\n"
        return task_list_str
    except Exception as e:
        return f"Error listing tasks: {e}"

# You should also add a function to create the table if it doesn't exist
# create_table_if_not_exists()