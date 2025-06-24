from database import Database 
from PySide6.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, 
    QListWidget, QListWidgetItem, QPushButton, QMessageBox
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.db = Database()  
        self.taskflow = self.db.get_all_tasks()  # Load tasks từ database
    
    def add_task(self, task):
        self.db.add_task(task)  # Thêm vào database trước
        self.taskflow = self.db.get_all_tasks()  # Load lại từ database
        self.update_task_list()
    
    def update_task(self, index, edited_task):
        task_id = self.db.get_task_id(self.taskflow[index])
        self.db.update_task(task_id, edited_task)
        self.taskflow = self.db.get_all_tasks()
        self.update_task_list()
    
    def delete_selected_task(self):
        selected_items = self.task_list_widget.selectedItems()
        selected_index = self.task_list_widget.row(selected_items[0])
        task_id = self.db.get_task_id(self.taskflow[selected_index])
        self.db.delete_task(task_id)
        self.taskflow = self.db.get_all_tasks()
        self.update_task_list()