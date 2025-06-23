from PySide6.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QWidget,
    QPushButton, QLabel, QListWidget, QListWidgetItem,
    QMessageBox, QMenu, QLineEdit, QCheckBox
)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QFont, QTextCharFormat, QTextCursor, QTextDocument
from add_task_dialog import AddTaskDialog
from database import DatabaseManager

class MainWindow(QMainWindow):
    def __init__(self, db_manager):
        """
        Khởi tạo cửa sổ chính của ứng dụng.
        Args:
            db_manager (DatabaseManager): Đối tượng quản lý cơ sở dữ liệu.
        """
        super().__init__()
        self.db_manager = db_manager
        self.setWindowTitle("Task Flow") # Đặt tiêu đề cửa sổ
        self.setGeometry(500, 200, 600, 500) # (x, y, width, height)
        # Widget trung tâm và layout chính
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Tiêu đề ứng dụng
        title_label = QLabel("TASK FLOW")
        title_font = QFont("Inter", 24, QFont.Bold) # Đặt font và kích thước
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter) # Căn giữa
        title_label.setStyleSheet("color: #2c3e50; padding: 10px;")
        main_layout.addWidget(title_label)

        # Nút "Thêm công việc mới"
        add_task_button = QPushButton("Thêm công việc mới")
        add_task_button.setFont(QFont("Inter", 12))
        add_task_button.setStyleSheet(
            "QPushButton { background-color: #3498db; color: white; padding: 10px 20px; border-radius: 8px; }"
            "QPushButton:hover { background-color: #2980b9; }"
        )
        add_task_button.clicked.connect(self.open_add_task_dialog)
        main_layout.addWidget(add_task_button)

        # Danh sách task
        self.task_list_widget = QListWidget()
        self.task_list_widget.setFont(QFont("Inter", 12))
        self.task_list_widget.setStyleSheet(
            "QListWidget { border: 1px solid #bdc3c7; border-radius: 8px; padding: 5px; background-color: #ecf0f1; }"
            "QListWidget::item { padding: 8px; margin-bottom: 5px; border-bottom: 1px solid #dfe6e9; }"
            "QListWidget::item:selected { background-color: #a0d2eb; color: #2c3e50; }"
        )
        # Bật menu ngữ cảnh
        self.task_list_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.task_list_widget.customContextMenuRequested.connect(self.show_context_menu)
        main_layout.addWidget(self.task_list_widget)

        # Bộ lọc
        filter_layout = QHBoxLayout()
        filter_label = QLabel("Bộ lọc:")
        filter_label.setFont(QFont("Inter", 10))
        filter_layout.addWidget(filter_label)

        self.all_tasks_button = QPushButton("Tất cả")
        self.pending_tasks_button = QPushButton("Đang làm")
        self.completed_tasks_button = QPushButton("Xong")

        # Áp dụng CSS cho các nút lọc
        button_style = (
            "QPushButton { background-color: #3498db; color: white; padding: 8px 15px; border-radius: 6px; border: none; }"
            "QPushButton:hover { background-color: #2980b9; }"
            "QPushButton:checked { background-color: #2c3e50; }" # Trạng thái khi được chọn
        )
        for btn in [self.all_tasks_button, self.pending_tasks_button, self.completed_tasks_button]:
            btn.setFont(QFont("Inter", 10))
            btn.setStyleSheet(button_style)
            btn.setCheckable(True) # Cho phép nút được chọn
            filter_layout.addWidget(btn)

        # Đặt nút "Tất cả" làm mặc định được chọn
        self.all_tasks_button.setChecked(True)

        filter_layout.addStretch() # Đẩy các nút sang trái
        main_layout.addLayout(filter_layout)

        # Kết nối tín hiệu cho các nút lọc
        self.all_tasks_button.clicked.connect(lambda: self.load_tasks("all"))
        self.pending_tasks_button.clicked.connect(lambda: self.load_tasks("pending"))
        self.completed_tasks_button.clicked.connect(lambda: self.load_tasks("completed"))

        # Khởi tạo dữ liệu khi ứng dụng bắt đầu
        self.load_tasks("all") # Tải tất cả task ban đầu

    def load_tasks(self, filter_status="all"):
        """
        Tải và hiển thị danh sách task từ cơ sở dữ liệu dựa trên trạng thái lọc.
        """
        # Đảm bảo chỉ một nút lọc được chọn tại một thời điểm
        for btn in [self.all_tasks_button, self.pending_tasks_button, self.completed_tasks_button]:
            if btn.text().lower().replace(' ', '') == filter_status.lower().replace(' ', ''):
                btn.setChecked(True)
            else:
                btn.setChecked(False)

        self.task_list_widget.clear() # Xóa các mục hiện có
        tasks = self.db_manager.get_tasks(filter_status)
        for task_id, name, description, deadline, completed in tasks:
            # Tạo một widget tùy chỉnh cho mỗi item trong list
            item_widget = QWidget()
            item_layout = QHBoxLayout(item_widget)
            item_layout.setContentsMargins(0, 0, 0, 0) # Xóa margin mặc định

            # Checkbox để đánh dấu hoàn thành
            checkbox = QCheckBox()
            checkbox.setChecked(completed == 1)
            checkbox.stateChanged.connect(lambda state, tid=task_id: self.toggle_task_completed_from_checkbox(tid, state))
            item_layout.addWidget(checkbox)

            # Label chứa tên task và deadline
            task_label_text = f"{name}"
            if deadline:
                task_label_text += f" - Deadline: {deadline}"
            
            task_label = QLabel(task_label_text)
            task_label.setFont(QFont("Inter", 12))
            
            if completed:
                font = task_label.font()
                font.setStrikeOut(True) # Gạch ngang nếu đã hoàn thành
                task_label.setFont(font)
                task_label.setStyleSheet("color: gray;")
            else:
                task_label.setStyleSheet("color: black;")
            
            item_layout.addWidget(task_label)
            item_layout.addStretch() # Đẩy checkbox và label sang trái

            # Tạo QListWidgetItem và thiết lập widget tùy chỉnh
            item = QListWidgetItem(self.task_list_widget)
            item.setSizeHint(item_widget.sizeHint()) # Đảm bảo kích thước đúng
            self.task_list_widget.addItem(item)
            self.task_list_widget.setItemWidget(item, item_widget)

            # Lưu dữ liệu task vào item để truy cập khi sửa/xóa
            item.setData(Qt.UserRole, task_id) 
            item.setData(Qt.UserRole + 1, name)
            item.setData(Qt.UserRole + 2, description)
            item.setData(Qt.UserRole + 3, deadline)
            item.setData(Qt.UserRole + 4, completed) # Lưu trạng thái completed

            print(f"Đã thêm item: {task_label_text} (ID: {task_id}, Completed: {completed})")

    def open_add_task_dialog(self, task_data=None):
        """
        Mở hộp thoại thêm/sửa task.
        Args:
            task_data (tuple, optional): Dữ liệu của task để sửa (id, name, desc, deadline, completed).
                                         Mặc định là None (thêm mới).
        """
        dialog = AddTaskDialog(task_data)
        if dialog.exec(): # Hiển thị hộp thoại và chờ cho đến khi nó đóng
            name, description, deadline, task_id = dialog.get_task_data()
            if task_id is None: # Thêm mới
                self.db_manager.add_task(name, description, deadline)
            else: # Sửa
                # Lấy trạng thái completed hiện tại để không bị mất khi sửa
                current_item = self.task_list_widget.currentItem()
                current_completed_status = 0
                if current_item:
                    # Tìm task ID trong list widget để lấy trạng thái completed
                    for i in range(self.task_list_widget.count()):
                        list_item = self.task_list_widget.item(i)
                        if list_item.data(Qt.UserRole) == task_id:
                            current_completed_status = list_item.data(Qt.UserRole + 4)
                            break
                self.db_manager.update_task(task_id, name, description, deadline, current_completed_status)
            self.load_tasks(self.get_current_filter_status()) # Tải lại task với bộ lọc hiện tại

    def get_current_filter_status(self):
        """Trả về trạng thái lọc hiện tại dựa trên nút nào đang được chọn."""
        if self.pending_tasks_button.isChecked():
            return "pending"
        elif self.completed_tasks_button.isChecked():
            return "completed"
        else:
            return "all"

    def show_context_menu(self, position):
        """
        Hiển thị menu ngữ cảnh khi nhấp chuột phải vào một item trong danh sách.
        """
        item = self.task_list_widget.itemAt(position)
        if item:
            menu = QMenu(self)

            # Lấy trạng thái hoàn thành của task từ data của QListWidgetItem
            task_completed = item.data(Qt.UserRole + 4)
            mark_action_text = "Đánh dấu chưa hoàn thành" if task_completed else "Đánh dấu hoàn thành"
            mark_action = menu.addAction(mark_action_text)
            mark_action.triggered.connect(lambda: self.toggle_task_completed_from_menu(item))

            edit_action = menu.addAction("Sửa")
            edit_action.triggered.connect(lambda: self.edit_task(item))

            delete_action = menu.addAction("Xóa")
            delete_action.triggered.connect(lambda: self.delete_task(item))

            menu.exec(self.task_list_widget.mapToGlobal(position))

    def edit_task(self, item):
        """
        Chỉnh sửa task đã chọn.
        """
        task_id = item.data(Qt.UserRole)
        name = item.data(Qt.UserRole + 1)
        description = item.data(Qt.UserRole + 2)
        deadline = item.data(Qt.UserRole + 3)
        completed = item.data(Qt.UserRole + 4) # Lấy trạng thái completed
        
        # Truyền cả ID và trạng thái completed để dialog có thể trả về đúng
        self.open_add_task_dialog((task_id, name, description, deadline, completed))

    def delete_task(self, item):
        """
        Xóa task đã chọn sau khi xác nhận.
        """
        task_id = item.data(Qt.UserRole)
        task_name = item.data(Qt.UserRole + 1) # Lấy tên task từ dữ liệu item

        reply = QMessageBox.question(
            self,
            "Xác nhận xóa",
            f"Bạn có chắc chắn muốn xóa task '{task_name}' không?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            if self.db_manager.delete_task(task_id):
                self.load_tasks(self.get_current_filter_status()) # Tải lại task sau khi xóa
            else:
                QMessageBox.critical(self, "Lỗi", "Không thể xóa task.")

    def toggle_task_completed_from_checkbox(self, task_id, state):
        """
        Chuyển đổi trạng thái hoàn thành của task khi checkbox thay đổi.
        """
        new_completed_status = 1 if state == Qt.Checked else 0
        if self.db_manager.mark_task_completed(task_id, new_completed_status):
            self.load_tasks(self.get_current_filter_status()) # Tải lại task sau khi cập nhật trạng thái
        else:
            QMessageBox.critical(self, "Lỗi", "Không thể cập nhật trạng thái task.")

    def toggle_task_completed_from_menu(self, item):
        """
        Chuyển đổi trạng thái hoàn thành của task từ menu ngữ cảnh.
        """
        task_id = item.data(Qt.UserRole)
        current_completed_status = item.data(Qt.UserRole + 4)
        new_completed_status = 1 if current_completed_status == 0 else 0

        if self.db_manager.mark_task_completed(task_id, new_completed_status):
            self.load_tasks(self.get_current_filter_status()) # Tải lại task sau khi cập nhật trạng thái
        else:
            QMessageBox.critical(self, "Lỗi", "Không thể cập nhật trạng thái task.")
