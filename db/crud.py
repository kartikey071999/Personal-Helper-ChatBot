import sqlite3
from typing import List, Tuple, Optional

DB_FILE = "tasks.db"

def get_db_connection():
    """Helper function to get a database connection."""
    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA foreign_keys = ON;")
    # conn.row_factory = sqlite3.Row  # Uncomment for dict-like row access
    return conn

# --- User CRUD ---

def create_user(username: str) -> Optional[int]:
    """Creates a new user and returns their ID."""
    sql = "INSERT INTO user (username) VALUES (?)"
    try:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute(sql, (username,))
        conn.commit()
        user_id = c.lastrowid
        conn.close()
        print(f"User '{username}' created with id {user_id}.")
        return user_id
    except sqlite3.IntegrityError:
        print(f"Error: Username '{username}' already exists.")
        return None
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return None

def get_user_by_id(user_id: int) -> Optional[Tuple]:
    """Fetches a user by their ID."""
    sql = "SELECT * FROM user WHERE id = ?"
    conn = get_db_connection()
    c = conn.cursor()
    c.execute(sql, (user_id,))
    user = c.fetchone()
    conn.close()
    return user

def get_all_users() -> List[Tuple]:
    """Fetches all users."""
    sql = "SELECT * FROM user"
    conn = get_db_connection()
    c = conn.cursor()
    c.execute(sql)
    users = c.fetchall()
    conn.close()
    return users

def delete_user(user_id: int) -> bool:
    """Deletes a user. Tasks will be unassigned via ON DELETE CASCADE."""
    sql = "DELETE FROM user WHERE id = ?"
    try:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute(sql, (user_id,))
        conn.commit()
        conn.close()
        print(f"User {user_id} deleted.")
        return True
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return False

# --- Task CRUD ---

def create_task(title: str, description: str = "") -> Optional[int]:
    """Creates a new task and returns its ID."""
    sql = "INSERT INTO task (title, description, status) VALUES (?, ?, 'todo')"
    try:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute(sql, (title, description))
        conn.commit()
        task_id = c.lastrowid
        conn.close()
        print(f"Task '{title}' created with id {task_id}.")
        return task_id
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return None

def get_task_by_id(task_id: int) -> Optional[Tuple]:
    """Fetches a task by its ID."""
    sql = "SELECT * FROM task WHERE id = ?"
    conn = get_db_connection()
    c = conn.cursor()
    c.execute(sql, (task_id,))
    task = c.fetchone()
    conn.close()
    return task

def update_task_status(task_id: int, status: str) -> bool:
    """Updates a task's status (e.g., 'todo', 'in_progress', 'done')."""
    sql = "UPDATE task SET status = ? WHERE id = ?"
    try:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute(sql, (status, task_id))
        conn.commit()
        conn.close()
        print(f"Task {task_id} status updated to '{status}'.")
        return True
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return False

def delete_task(task_id: int) -> bool:
    """Deletes a task. Assignments will be removed via ON DELETE CASCADE."""
    sql = "DELETE FROM task WHERE id = ?"
    try:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute(sql, (task_id,))
        conn.commit()
        conn.close()
        print(f"Task {task_id} deleted.")
        return True
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return False

# --- Relationship CRUD ---

def assign_task_to_user(user_id: int, task_id: int) -> bool:
    """Assigns a task to a user."""
    sql = "INSERT INTO task_user_relationship (user_id, task_id) VALUES (?, ?)"
    try:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute(sql, (user_id, task_id))
        conn.commit()
        conn.close()
        print(f"Task {task_id} assigned to user {user_id}.")
        return True
    except sqlite3.IntegrityError:
        print(f"Error: Task {task_id} is already assigned to user {user_id}.")
        return False
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return False

def unassign_task_from_user(user_id: int, task_id: int) -> bool:
    """Unassigns a task from a user."""
    sql = "DELETE FROM task_user_relationship WHERE user_id = ? AND task_id = ?"
    try:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute(sql, (user_id, task_id))
        conn.commit()
        conn.close()
        print(f"Task {task_id} unassigned from user {user_id}.")
        return True
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return False

def get_tasks_for_user(user_id: int) -> List[Tuple]:
    """Gets all tasks assigned to a specific user."""
    sql = """
    SELECT task.id, task.title, task.description, task.status
    FROM task
    JOIN task_user_relationship ON task.id = task_user_relationship.task_id
    WHERE task_user_relationship.user_id = ?
    """
    conn = get_db_connection()
    c = conn.cursor()
    c.execute(sql, (user_id,))
    tasks = c.fetchall()
    conn.close()
    return tasks

def get_users_for_task(task_id: int) -> List[Tuple]:
    """Gets all users assigned to a specific task."""
    sql = """
    SELECT user.id, user.username
    FROM user
    JOIN task_user_relationship ON user.id = task_user_relationship.user_id
    WHERE task_user_relationship.task_id = ?
    """
    conn = get_db_connection()
    c = conn.cursor()
    c.execute(sql, (task_id,))
    users = c.fetchall()
    conn.close()
    return users


# --- Example Usage ---

if __name__ == "__main__":
    print("Running DB operations test...")
    
    # Note: Make sure you've run db_setup.py at least once!
    
    # Create users
    user1_id = create_user("kartikey")
    user2_id = create_user("jane_doe")
    
    # Create tasks
    task1_id = create_task("Build chatbot", "Use Gemini and SQLite")
    task2_id = create_task("Buy groceries", "Milk, eggs, bread")
    
    if user1_id and task1_id and task2_id:
        # Assign tasks
        assign_task_to_user(user1_id, task1_id)
        assign_task_to_user(user1_id, task2_id)
    
    if user2_id and task2_id:
        assign_task_to_user(user2_id, task2_id)

    # Read operations
    if user1_id:
        print(f"\n--- Tasks for user {user1_id} (kartikey) ---")
        kartikey_tasks = get_tasks_for_user(user1_id)
        for task in kartikey_tasks:
            print(task)

    if task2_id:
        print(f"\n--- Users for task {task2_id} (Buy groceries) ---")
        groceries_users = get_users_for_task(task2_id)
        for user in groceries_users:
            print(user)
    
    # Update operation
    if task1_id:
        print("\n--- Updating task status ---")
        update_task_status(task1_id, "in_progress")
        print(get_task_by_id(task1_id))

    # Delete operation
    if task1_id:
        print("\n--- Deleting task ---")
        delete_task(task1_id)
        print(f"Kartikey's tasks after deletion: {get_tasks_for_user(user1_id)}")

    print("\nTest complete.")