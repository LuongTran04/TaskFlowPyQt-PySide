from PySide6.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, 
    QListWidget, QListWidgetItem, QPushButton, QMessageBox
)
from PySide6.QtCore import Qt
from add_task_window import AddTaskWindow
from edit_task_window import EditTaskWindow
from task import Task

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TaskFlow")
        self.setGeometry(500, 200, 600, 400)
        
        self.tasks = []
        
        self.init_ui()
        
    def init_ui(self):
        # Màn hình chính 
        main_layout = QVBoxLayout()
        
        title_label = QLabel("Task List")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; margin: 10px;")
        main_layout.addWidget(title_label)
        
        # Nút bấm 
        buttons_layout = QHBoxLayout()
        
        # Nút thêm task
        self.add_button = QPushButton("Add Task")
        self.add_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.add_button.clicked.connect(self.open_add_task_window)
        buttons_layout.addWidget(self.add_button)
        
        # Nút sửa task
        self.edit_button = QPushButton("Edit Task")
        self.edit_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #0b7dda;
            }
        """)
        self.edit_button.clicked.connect(self.edit_selected_task)
        buttons_layout.addWidget(self.edit_button)
        
        # Nút xóa task
        self.delete_button = QPushButton("Delete Task")
        self.delete_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        """)
        self.delete_button.clicked.connect(self.delete_selected_task)
        buttons_layout.addWidget(self.delete_button)
        
        main_layout.addLayout(buttons_layout)

        # Danh sách task
        self.task_list_widget = QListWidget()
        self.task_list_widget.setStyleSheet("""
            QListWidget {
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 5px;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #ddd;
            }
            QListWidget::item:hover {
                background-color: #e9e9e9;
            }
        """)
        main_layout.addWidget(self.task_list_widget)
        
        
        # Thiết lập layout cho màn hình chính
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        
    def open_add_task_window(self):
        self.add_task_window = AddTaskWindow()
        self.add_task_window.task_added.connect(self.add_task)
        self.add_task_window.show()
        
    def add_task(self, task):
        self.tasks.append(task)
        self.update_task_list()
        
    def edit_selected_task(self):
        selected_items = self.task_list_widget.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Warning", "Please select a task to edit.")
            return
            
        selected_index = self.task_list_widget.row(selected_items[0])
        task_to_edit = self.tasks[selected_index]
        
        self.edit_task_window = EditTaskWindow(task_to_edit)
        self.edit_task_window.task_edited.connect(lambda edited_task: self.update_task(selected_index, edited_task))
        self.edit_task_window.show()
        
    def update_task(self, index, edited_task):
        self.tasks[index] = edited_task
        self.update_task_list()
        
    def delete_selected_task(self):
        selected_items = self.task_list_widget.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Warning", "Please select a task to delete.")
            return
            
        selected_index = self.task_list_widget.row(selected_items[0])
        
        reply = QMessageBox.question(
            self, 
            "Delete Task", 
            "Are you sure you want to delete this task?", 
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            del self.tasks[selected_index]
            self.update_task_list()
        
    def update_task_list(self):
        self.task_list_widget.clear()
        for task in self.tasks:
            item = QListWidgetItem(f"{task.name} - Description: {task.description} - Due: {task.due_date}")
            item.setData(Qt.ItemDataRole.UserRole, task)
            self.task_list_widget.addItem(item)