import sqlite3
import os # Import module os để kiểm tra sự tồn tại của file database

class DatabaseManager:
    def __init__(self, db_name="tasks.db"):
        """
        Khởi tạo DatabaseManager.
        Nếu file database không tồn tại, nó sẽ được tạo.
        Sau đó, bảng 'tasks' sẽ được tạo nếu nó chưa tồn tại.
        """
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self._connect()
        self._create_table()

    def _connect(self):
        """Kết nối đến cơ sở dữ liệu SQLite."""
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            print(f"Đã kết nối thành công tới database: {self.db_name}")
        except sqlite3.Error as e:
            print(f"Lỗi kết nối database: {e}")

    def _create_table(self):
        """
        Tạo bảng 'tasks' nếu nó chưa tồn tại.
        Nếu gặp lỗi liên quan đến bảng (ví dụ: syntax error), hãy thử xóa file 'tasks.db' và chạy lại ứng dụng.
        """
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    deadline TEXT, -- Định dạng YYYY-MM-DD
                    completed INTEGER DEFAULT 0 -- 0: chưa hoàn thành, 1: hoàn thành
                )
            """)
            self.conn.commit()
            print("Đã kiểm tra/tạo bảng 'tasks'.")
        except sqlite3.Error as e:
            print(f"Lỗi khi tạo bảng: {e}. Vui lòng thử xóa file 'tasks.db' và chạy lại.")

    def add_task(self, name, description, deadline):
        """
        Thêm một task mới vào cơ sở dữ liệu.
        Trả về ID của task vừa thêm hoặc None nếu có lỗi.
        """
        try:
            self.cursor.execute(
                "INSERT INTO tasks (name, description, deadline, completed) VALUES (?, ?, ?, ?)",
                (name, description, deadline, 0) # Mặc định completed là 0 (chưa hoàn thành)
            )
            self.conn.commit()
            print(f"Đã thêm task: {name}")
            return self.cursor.lastrowid # Trả về ID của hàng cuối cùng được chèn
        except sqlite3.Error as e:
            print(f"Lỗi khi thêm task: {e}")
            return None

    def get_tasks(self, filter_status="all"):
        """
        Lấy danh sách các task từ cơ sở dữ liệu dựa trên trạng thái lọc.
        filter_status có thể là 'all', 'pending' (đang làm), 'completed' (đã xong).
        """
        query = "SELECT id, name, description, deadline, completed FROM tasks"
        params = []
        if filter_status == "pending":
            query += " WHERE completed = 0"
        elif filter_status == "completed":
            query += " WHERE completed = 1"
        query += " ORDER BY deadline ASC, id DESC" # Sắp xếp theo deadline và ID (mới nhất lên đầu)

        try:
            self.cursor.execute(query, params)
            tasks = self.cursor.fetchall()
            print(f"Đã lấy {len(tasks)} task với bộ lọc '{filter_status}'.")
            return tasks
        except sqlite3.Error as e:
            print(f"Lỗi khi lấy task: {e}")
            return []

    def update_task(self, task_id, name, description, deadline, completed):
        """
        Cập nhật thông tin của một task trong cơ sở dữ liệu.
        """
        try:
            self.cursor.execute(
                "UPDATE tasks SET name = ?, description = ?, deadline = ?, completed = ? WHERE id = ?",
                (name, description, deadline, completed, task_id)
            )
            self.conn.commit()
            print(f"Đã cập nhật task ID: {task_id}")
            return True
        except sqlite3.Error as e:
            print(f"Lỗi khi cập nhật task ID {task_id}: {e}")
            return False

    def delete_task(self, task_id):
        """
        Xóa một task khỏi cơ sở dữ liệu.
        """
        try:
            self.cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            self.conn.commit()
            print(f"Đã xóa task ID: {task_id}")
            return True
        except sqlite3.Error as e:
            print(f"Lỗi khi xóa task ID {task_id}: {e}")
            return False

    def mark_task_completed(self, task_id, completed_status):
        """
        Đánh dấu một task là hoàn thành (1) hoặc chưa hoàn thành (0).
        """
        try:
            self.cursor.execute(
                "UPDATE tasks SET completed = ? WHERE id = ?",
                (completed_status, task_id)
            )
            self.conn.commit()
            print(f"Đã cập nhật trạng thái hoàn thành cho task ID {task_id} thành {completed_status}.")
            return True
        except sqlite3.Error as e:
            print(f"Lỗi khi cập nhật trạng thái hoàn thành cho task ID {task_id}: {e}")
            return False

    def close(self):
        """Đóng kết nối cơ sở dữ liệu."""
        if self.conn:
            self.conn.close()
            print("Đã đóng kết nối database.")