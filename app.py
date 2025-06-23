import sys
from PySide6.QtWidgets import QApplication
from main_window import MainWindow
from database import DatabaseManager

if __name__ == "__main__":
    # Tạo một đối tượng QApplication.
    # sys.argv là danh sách các đối số dòng lệnh được truyền cho tập lệnh Python.
    app = QApplication(sys.argv)

    # Khởi tạo DatabaseManager. Nó sẽ kết nối đến database và tạo bảng nếu chưa có.
    db_manager = DatabaseManager("tasks.db")

    # Tạo cửa sổ chính của ứng dụng, truyền vào đối tượng quản lý database.
    main_window = MainWindow(db_manager)

    # Hiển thị cửa sổ chính.
    main_window.show()

    # Bắt đầu vòng lặp sự kiện của ứng dụng.
    # Phương thức exec() sẽ giữ ứng dụng chạy cho đến khi người dùng đóng cửa sổ.
    sys.exit(app.exec())