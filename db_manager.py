from PySide6.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, 
    QListWidget, QListWidgetItem, QPushButton, QMessageBox
)
from PySide6.QtCore import Qt

import sqlite3
from task import Task

class Database:
    def __init__(self, db_name="taskflow.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    # Tạo bảng nếu chưa tồn tại
    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            due_date TEXT,
            description TEXT,
            completed INTEGER DEFAULT 0
        );
        """
        self.conn.execute(query)
        self.conn.commit()

    def add_task(self, task: Task):
        query = "INSERT INTO tasks (name, due_date, description, completed) VALUES (?, ?, ?, ?)"
        self.conn.execute(query, (task.name, task.due_date, task.description, 0))
        self.conn.commit()

    def get_all_tasks(self):
        cursor = self.conn.execute("SELECT id, name, due_date, description, completed FROM tasks")
        tasks = []
        for row in cursor:
            task = Task(name=row[1], due_date=row[2], description=row[3])
            task.id = row[0]
            task.completed = bool(row[4])
            tasks.append(task)
        return tasks

    def get_task_id(self, task: Task):
        cursor = self.conn.execute("SELECT id FROM tasks WHERE name = ? AND due_date = ? AND description = ?", (task.name, task.due_date, task.description))
        row = cursor.fetchone()
        return row[0] if row else None

    def update_task(self, task_id: int, task: Task):
        query = "UPDATE tasks SET name = ?, due_date = ?, description = ? WHERE id = ?"
        self.conn.execute(query, (task.name, task.due_date, task.description, task_id))
        self.conn.commit()

    def delete_task(self, task_id: int):
        self.conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        self.conn.commit()

    def mark_task_completed(self, task_id: int):
        try:
            self.conn.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,))
            self.conn.commit()
            return True
        except:
            return False
