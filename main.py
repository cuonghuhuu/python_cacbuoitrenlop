import sys
from typing import Any, Iterable, Optional

import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
from PyQt5 import uic
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
    QTableWidgetItem,
)

UI_FILE = "hr_manager.ui"


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        uic.loadUi(UI_FILE, self)
        self.conn = None
        self.setup_signals()
        self.log(
            "Ứng dụng đã sẵn sàng.\n"
            "Lưu ý: code này giả định schema gần giống HR sample:\n"
            "- department(department_id, department_name, manager_id, location_id)\n"
            "- employee(employee_id, first_name, last_name, email, phone_number, hire_date, job_id, salary, commission_pct, manager_id, department_id)"
        )

    def setup_signals(self) -> None:
        self.btnConnect.clicked.connect(self.connect_db)
        self.btnLoadManagers.clicked.connect(self.load_managers)
        self.btnInsertDepartment.clicked.connect(self.insert_department)
        self.btnInsertEmployee.clicked.connect(self.insert_employee)
        self.btnUpdateClark.clicked.connect(self.update_clark)
        self.btnDeleteMiller.clicked.connect(self.delete_miller)

    def log(self, message: str) -> None:
        self.txtLog.append(message)
        self.statusbar.showMessage(message, 5000)

    def show_error(self, title: str, message: str) -> None:
        QMessageBox.critical(self, title, message)
        self.log(f"[LỖI] {message}")

    def show_info(self, title: str, message: str) -> None:
        QMessageBox.information(self, title, message)
        self.log(f"[OK] {message}")

    def connect_db(self) -> None:
        try:
            if self.conn:
                self.conn.close()

            self.conn = psycopg2.connect(
                host=self.txtHost.text().strip(),
                port=self.txtPort.text().strip(),
                dbname=self.txtDbName.text().strip(),
                user=self.txtUser.text().strip(),
                password=self.txtPassword.text(),
            )
            self.conn.autocommit = False
            self.show_info("Kết nối", "Kết nối PostgreSQL thành công.")
        except Exception as e:
            self.show_error("Kết nối thất bại", str(e))

    def ensure_connection(self) -> bool:
        if not self.conn:
            self.show_error("Chưa kết nối", "Bạn cần kết nối PostgreSQL trước.")
            return False
        return True

    def fetch_rows(self, query: str, params: Optional[Iterable[Any]] = None):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, params)
            return cur.fetchall()

    def execute_query(self, query: str, params: Optional[Iterable[Any]] = None) -> int:
        with self.conn.cursor() as cur:
            cur.execute(query, params)
            return cur.rowcount

    def set_table_data(self, rows) -> None:
        self.tableManagers.clear()
        if not rows:
            self.tableManagers.setRowCount(0)
            self.tableManagers.setColumnCount(0)
            self.log("Không có dữ liệu để hiển thị.")
            return

        headers = list(rows[0].keys())
        self.tableManagers.setColumnCount(len(headers))
        self.tableManagers.setHorizontalHeaderLabels(headers)
        self.tableManagers.setRowCount(len(rows))

        for row_idx, row in enumerate(rows):
            for col_idx, key in enumerate(headers):
                value = "" if row[key] is None else str(row[key])
                self.tableManagers.setItem(row_idx, col_idx, QTableWidgetItem(value))

        self.tableManagers.resizeColumnsToContents()

    def load_managers(self) -> None:
        if not self.ensure_connection():
            return

        query = """
            SELECT employee_id, first_name, last_name, email, phone_number, job_id, salary, department_id
            FROM employee
            WHERE UPPER(job_id) LIKE '%MAN%'
               OR UPPER(job_id) LIKE '%MGR%'
               OR UPPER(job_id) = 'MANAGER'
            ORDER BY employee_id;
        """
        try:
            rows = self.fetch_rows(query)
            self.set_table_data(rows)
            self.log(f"Đã tải {len(rows)} nhân viên có chức vụ MANAGER/MGR.")
        except Exception as e:
            self.show_error(
                "Lỗi truy vấn",
                f"Không lấy được danh sách manager.\n{e}\n\n"
                "Nếu schema của bạn dùng cột khác job_id thì sửa lại câu SQL trong hàm load_managers().",
            )

    def insert_department(self) -> None:
        if not self.ensure_connection():
            return

        try:
            query = """
                INSERT INTO department (department_id, department_name, manager_id, location_id)
                VALUES (%s, %s, %s, %s);
            """
            params = (
                self.txtDeptId.text().strip(),
                self.txtDeptName.text().strip(),
                self.nullable_int(self.txtDeptManagerId.text()),
                self.nullable_int(self.txtDeptLocationId.text()),
            )
            self.execute_query(query, params)
            self.conn.commit()
            self.show_info("Insert Department", "Đã thêm department thành công.")
        except Exception as e:
            self.conn.rollback()
            self.show_error("Insert Department thất bại", str(e))

    def insert_employee(self) -> None:
        if not self.ensure_connection():
            return

        try:
            query = """
                INSERT INTO employee (
                    employee_id, first_name, last_name, email, phone_number,
                    hire_date, job_id, salary, commission_pct, manager_id, department_id
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """
            params = (
                self.txtEmpId.text().strip(),
                self.txtFirstName.text().strip(),
                self.txtLastName.text().strip(),
                self.txtEmail.text().strip(),
                self.txtPhone.text().strip(),
                self.txtHireDate.text().strip(),
                self.txtJobId.text().strip(),
                self.nullable_float(self.txtSalary.text()),
                self.nullable_float(self.txtCommissionPct.text()),
                self.nullable_int(self.txtManagerId.text()),
                self.nullable_int(self.txtDepartmentId.text()),
            )
            self.execute_query(query, params)
            self.conn.commit()
            self.show_info("Insert Employee", "Đã thêm employee thành công.")
        except Exception as e:
            self.conn.rollback()
            self.show_error("Insert Employee thất bại", str(e))

    def update_clark(self) -> None:
        if not self.ensure_connection():
            return

        try:
            query = """
                UPDATE employee
                SET first_name = %s,
                    last_name = %s,
                    email = %s,
                    phone_number = %s,
                    hire_date = %s,
                    job_id = %s,
                    salary = %s,
                    commission_pct = %s,
                    manager_id = %s,
                    department_id = %s
                WHERE UPPER(last_name) = 'CLARK';
            """
            params = (
                self.txtUFirstName.text().strip(),
                self.txtULastName.text().strip(),
                self.txtUEmail.text().strip(),
                self.txtUPhone.text().strip(),
                self.txtUHireDate.text().strip(),
                self.txtUJobId.text().strip(),
                self.nullable_float(self.txtUSalary.text()),
                self.nullable_float(self.txtUCommissionPct.text()),
                self.nullable_int(self.txtUManagerId.text()),
                self.nullable_int(self.txtUDepartmentId.text()),
            )
            affected = self.execute_query(query, params)
            self.conn.commit()
            if affected == 0:
                self.show_info("Update CLARK", "Không tìm thấy nhân viên CLARK để cập nhật.")
            else:
                self.show_info("Update CLARK", f"Đã cập nhật {affected} dòng có last_name = CLARK.")
        except Exception as e:
            self.conn.rollback()
            self.show_error("Update CLARK thất bại", str(e))

    def delete_miller(self) -> None:
        if not self.ensure_connection():
            return

        reply = QMessageBox.question(
            self,
            "Xác nhận xóa",
            "Bạn có chắc muốn xóa nhân viên MILLER không?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if reply != QMessageBox.Yes:
            self.log("Đã hủy thao tác xóa MILLER.")
            return

        try:
            query = "DELETE FROM employee WHERE UPPER(last_name) = 'MILLER';"
            affected = self.execute_query(query)
            self.conn.commit()
            if affected == 0:
                self.show_info("Delete MILLER", "Không tìm thấy nhân viên MILLER để xóa.")
            else:
                self.show_info("Delete MILLER", f"Đã xóa {affected} dòng có last_name = MILLER.")
        except Exception as e:
            self.conn.rollback()
            self.show_error("Delete MILLER thất bại", str(e))

    @staticmethod
    def nullable_int(value: str):
        value = value.strip()
        return None if value == "" else int(value)

    @staticmethod
    def nullable_float(value: str):
        value = value.strip()
        return None if value == "" else float(value)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
