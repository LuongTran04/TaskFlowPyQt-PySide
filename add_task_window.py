from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QComboBox, 
    QDateEdit, QPushButton, QMessageBox
)
from PySide6.QtCore import Qt, QDate, Signal
from task import Task

class AddTaskWindow(QWidget):
    task_added = Signal(Task)
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add New Task")
        self.setGeometry(650, 300, 300, 250)
        
        self.init_ui()

    # Hàm giao diện thêm task    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Tên task
        layout.addWidget(QLabel("Task Name:"))
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter task name")
        layout.addWidget(self.name_input)
        
        # Deadline
        layout.addWidget(QLabel("Due Date:"))
        self.due_date_input = QDateEdit()
        self.due_date_input.setCalendarPopup(True)
        self.due_date_input.setDate(QDate.currentDate())
        layout.addWidget(self.due_date_input)
        
        # Mô tả
        layout.addWidget(QLabel("Description:"))
        self.description_input = QLineEdit()
        self.description_input.setPlaceholderText("Optional task description")
        layout.addWidget(self.description_input)
        
        # Nút thêm task
        add_button = QPushButton("Add Task")
        add_button.clicked.connect(self.add_task)
        layout.addWidget(add_button)
        
        self.setLayout(layout)

    # Hàm để thêm task    
    def add_task(self):
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Warning", "Task name cannot be empty!")
            return
            
        new_task = Task(
            name=name,
            due_date=self.due_date_input.date().toString("yyyy-MM-dd"),
            description=self.description_input.text()
        )
        
        self.task_added.emit(new_task)
        self.close()