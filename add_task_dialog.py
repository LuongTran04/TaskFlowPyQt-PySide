from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QTextEdit, QPushButton, QDateEdit, QMessageBox
)
from PySide6.QtCore import Qt, QDate

class AddTaskDialog(QDialog):
    def __init__(self, task_data=None):
        """
        Khởi tạo hộp thoại thêm/sửa task.
        Args:
            task_data (tuple, optional): Dữ liệu của task để điền vào (id, name, desc, deadline, completed).
                                         Nếu None, đây là form thêm mới.
        """
        super().__init__()
        self.task_data = task_data # Lưu trữ dữ liệu task nếu là chế độ sửa
        self.task_id = task_data[0] if task_data else None

        if task_data:
            self.setWindowTitle("Sửa Task")
        else:
            self.setWindowTitle("Tạo Task Mới")

        self.setGeometry(500, 200, 400, 300) # (x, y, width, height)

        main_layout = QVBoxLayout(self)

        # Tên task
        main_layout.addWidget(QLabel("Tên công việc:"))
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nhập tên công việc")
        self.name_input.setStyleSheet("padding: 8px; border: 1px solid #bdc3c7; border-radius: 5px;")
        main_layout.addWidget(self.name_input)

        # Mô tả
        main_layout.addWidget(QLabel("Mô tả:"))
        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("Nhập mô tả (tùy chọn)")
        self.description_input.setStyleSheet("padding: 8px; border: 1px solid #bdc3c7; border-radius: 5px;")
        main_layout.addWidget(self.description_input)

        # Deadline
        main_layout.addWidget(QLabel("Deadline (DD/MM/YYYY):"))
        self.deadline_input = QDateEdit(QDate.currentDate())
        self.deadline_input.setCalendarPopup(True) # Cho phép chọn ngày từ popup lịch
        self.deadline_input.setDisplayFormat("dd/MM/yyyy") # Định dạng hiển thị
        self.deadline_input.setStyleSheet("padding: 8px; border: 1px solid #bdc3c7; border-radius: 5px;")
        main_layout.addWidget(self.deadline_input)

        # Nút Tạo/Cập nhật và Hủy
        button_layout = QHBoxLayout()
        self.create_update_button = QPushButton("Tạo Task" if task_data is None else "Cập nhật Task")
        self.create_update_button.setStyleSheet(
            "QPushButton { background-color: #3498db; color: white; padding: 10px 20px; border-radius: 8px; }"
            "QPushButton:hover { background-color: #2980b9; }"
        )
        self.create_update_button.clicked.connect(self.accept_data) # Kết nối với hàm xử lý dữ liệu
        button_layout.addWidget(self.create_update_button)

        cancel_button = QPushButton("Hủy")
        cancel_button.setStyleSheet(
            "QPushButton { background-color: #dc3545; color: white; padding: 10px 20px; border-radius: 8px; }"
            "QPushButton:hover { background-color: #c82333; }"
        )
        cancel_button.clicked.connect(self.reject) # Kết nối với hàm hủy của QDialog
        button_layout.addWidget(cancel_button)

        main_layout.addLayout(button_layout)

        # Nếu đang ở chế độ sửa, điền dữ liệu cũ vào các trường
        if self.task_data:
            self.name_input.setText(self.task_data[1])
            self.description_input.setText(self.task_data[2] if self.task_data[2] else "")
            if self.task_data[3]: # Nếu có deadline
                deadline_date = QDate.fromString(self.task_data[3], "yyyy-MM-dd")
                self.deadline_input.setDate(deadline_date)
            else: # Nếu không có deadline, đặt là ngày hiện tại
                self.deadline_input.setDate(QDate.currentDate())


    def accept_data(self):
        """
        Kiểm tra dữ liệu nhập vào và chấp nhận nếu hợp lệ.
        """
        name = self.name_input.text().strip()
        description = self.description_input.toPlainText().strip()
        deadline = self.deadline_input.date().toString("yyyy-MM-dd") # Lưu dưới định dạng YYYY-MM-DD

        if not name:
            QMessageBox.warning(self, "Lỗi", "Tên task không được để trống!")
            return

        self.accept() # Chấp nhận hộp thoại, đóng nó và trả về QDialog.Accepted

    def get_task_data(self):
        """
        Trả về dữ liệu task đã nhập từ form.
        """
        name = self.name_input.text().strip()
        description = self.description_input.toPlainText().strip()
        deadline = self.deadline_input.date().toString("yyyy-MM-dd")
        return name, description, deadline, self.task_id # Trả về cả ID để biết là thêm hay sửa
