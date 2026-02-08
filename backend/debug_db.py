import sqlite3
import hashlib

# Connect to the database to check if tables exist
conn = sqlite3.connect('todo_app.db')
cursor = conn.cursor()

# Check if tables exist
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables in database:", tables)

# Check the schema of the user table if it exists
if ('user',) in tables:
    cursor.execute("PRAGMA table_info(user)")
    user_schema = cursor.fetchall()
    print("User table schema:", user_schema)

# Check the schema of the task table if it exists
if ('task',) in tables:
    cursor.execute("PRAGMA table_info(task)")
    task_schema = cursor.fetchall()
    print("Task table schema:", task_schema)

conn.close()