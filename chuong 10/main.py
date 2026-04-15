import sys
import re
import sqlite3
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import (
    QMessageBox,
    QGraphicsDropShadowEffect,
    QTableWidgetItem
)
from PyQt6.QtGui import QColor


DB_NAME = "data.db"

app = QtWidgets.QApplication(sys.argv)
window = uic.loadUi("dangky.ui")
form_ds = None


def tao_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS thanhvien (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ho TEXT NOT NULL,
            ten TEXT NOT NULL,
            lien_he TEXT NOT NULL,
            mat_khau TEXT NOT NULL,
            ngay_sinh TEXT NOT NULL,
            gioi_tinh TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def giao_dien_dep():
    window.setWindowTitle("Đăng ký thành viên")

    window.setStyleSheet("""
        QLabel {
            font-size: 14px;
        }

        QLineEdit, QComboBox {
            font-size: 14px;
            padding: 6px;
            border: 1px solid #cfcfcf;
            border-radius: 8px;
        }

        QLineEdit:focus, QComboBox:focus {
            border: 1px solid #4a90e2;
        }

        QRadioButton, QCheckBox {
            font-size: 13px;
        }

        QPushButton {
            background-color: #111111;
            color: white;
            font-size: 15px;
            font-weight: bold;
            border: none;
            border-radius: 10px;
            padding: 8px 16px;
        }

        QPushButton:hover {
            background-color: #333333;
        }

        QPushButton:pressed {
            background-color: #000000;
        }
    """)

    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(20)
    shadow.setXOffset(3)
    shadow.setYOffset(4)
    shadow.setColor(QColor(0, 0, 0, 120))
    window.btnDangKy.setGraphicsEffect(shadow)

    window.txtMatKhau.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)


def khoi_tao_ngay_sinh():
    window.cboNgay.clear()
    window.cboThang.clear()
    window.cboNam.clear()

    for i in range(1, 32):
        window.cboNgay.addItem(str(i))

    for i in range(1, 13):
        window.cboThang.addItem(str(i))

    for i in range(1970, 2026):
        window.cboNam.addItem(str(i))


def kiem_tra_mat_khau(mat_khau: str) -> bool:
    if len(mat_khau) < 8:
        return False
    if not re.search(r"[a-z]", mat_khau):
        return False
    if not re.search(r"[A-Z]", mat_khau):
        return False
    if not re.search(r"[0-9]", mat_khau):
        return False
    if not re.search(r"[^A-Za-z0-9]", mat_khau):
        return False
    return True


def xoa_form():
    window.txtHo.clear()
    window.txtTen.clear()
    window.txtLienHe.clear()
    window.txtMatKhau.clear()
    window.radNam.setChecked(False)
    window.radNu.setChecked(False)
    window.chkDongY.setChecked(False)
    window.cboNgay.setCurrentIndex(0)
    window.cboThang.setCurrentIndex(0)
    window.cboNam.setCurrentIndex(0)
    window.txtHo.setFocus()


def luu_thanh_vien(ho, ten, lien_he, mat_khau, ngay_sinh, gioi_tinh):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO thanhvien (ho, ten, lien_he, mat_khau, ngay_sinh, gioi_tinh)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (ho, ten, lien_he, mat_khau, ngay_sinh, gioi_tinh))
    conn.commit()
    conn.close()


def lay_danh_sach_thanh_vien():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, ho, ten, lien_he, mat_khau, ngay_sinh, gioi_tinh
        FROM thanhvien
        ORDER BY id DESC
    """)
    data = cursor.fetchall()
    conn.close()
    return data


def mo_danh_sach():
    global form_ds

    form_ds = uic.loadUi("danhsach.ui")
    form_ds.setWindowTitle("Danh sách thành viên")

    data = lay_danh_sach_thanh_vien()

    form_ds.tableThanhVien.setRowCount(len(data))
    form_ds.tableThanhVien.setColumnCount(7)
    form_ds.tableThanhVien.setHorizontalHeaderLabels([
        "ID", "Họ", "Tên", "Liên hệ", "Mật khẩu", "Ngày sinh", "Giới tính"
    ])

    for row, item in enumerate(data):
        for col, value in enumerate(item):
            form_ds.tableThanhVien.setItem(row, col, QTableWidgetItem(str(value)))

    form_ds.tableThanhVien.resizeColumnsToContents()

    if hasattr(form_ds, "btnDong"):
        form_ds.btnDong.clicked.connect(form_ds.close)

    form_ds.show()


def dang_ky():
    ho = window.txtHo.text().strip()
    ten = window.txtTen.text().strip()
    lien_he = window.txtLienHe.text().strip()
    mat_khau = window.txtMatKhau.text().strip()

    gioi_tinh = ""
    if window.radNam.isChecked():
        gioi_tinh = "Nam"
    elif window.radNu.isChecked():
        gioi_tinh = "Nữ"

    ngay_sinh = f"{window.cboNgay.currentText()}/{window.cboThang.currentText()}/{window.cboNam.currentText()}"

    if ho == "":
        QMessageBox.warning(window, "Lỗi", "Vui lòng nhập họ.")
        window.txtHo.setFocus()
        return

    if ten == "":
        QMessageBox.warning(window, "Lỗi", "Vui lòng nhập tên.")
        window.txtTen.setFocus()
        return

    if lien_he == "":
        QMessageBox.warning(window, "Lỗi", "Vui lòng nhập số điện thoại hoặc email.")
        window.txtLienHe.setFocus()
        return

    if mat_khau == "":
        QMessageBox.warning(window, "Lỗi", "Vui lòng nhập mật khẩu.")
        window.txtMatKhau.setFocus()
        return

    if gioi_tinh == "":
        QMessageBox.warning(window, "Lỗi", "Vui lòng chọn giới tính.")
        return

    if not window.chkDongY.isChecked():
        QMessageBox.warning(window, "Lỗi", "Bạn phải đồng ý với các điều khoản.")
        return

    if not kiem_tra_mat_khau(mat_khau):
        QMessageBox.warning(
            window,
            "Lỗi",
            "Mật khẩu phải có ít nhất 8 ký tự, gồm chữ thường, chữ hoa, số và ký tự đặc biệt."
        )
        window.txtMatKhau.setFocus()
        return

    luu_thanh_vien(ho, ten, lien_he, mat_khau, ngay_sinh, gioi_tinh)

    QMessageBox.information(
        window,
        "Thành công",
        f"Đăng ký thành công!\n\n"
        f"Họ tên: {ho} {ten}\n"
        f"Liên hệ: {lien_he}\n"
        f"Ngày sinh: {ngay_sinh}\n"
        f"Giới tính: {gioi_tinh}"
    )

    xoa_form()
    mo_danh_sach()


tao_database()
giao_dien_dep()
khoi_tao_ngay_sinh()
window.btnDangKy.clicked.connect(dang_ky)

window.show()
app.exec()