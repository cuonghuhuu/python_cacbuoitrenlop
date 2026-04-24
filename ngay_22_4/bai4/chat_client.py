"""
Bai 4 - Chat Client GUI

Chay file:
    python chat_client.py
"""

import socket
import threading
from pathlib import Path

try:
    from PyQt5 import QtCore, QtWidgets, uic
except ImportError as error:
    raise SystemExit(
        "PyQt5 chua duoc cai dat. Cai bang lenh: pip install PyQt5"
    ) from error


PORT = 8093
BUFFER_SIZE = 1024
DEFAULT_HOST = "127.0.0.1"
UI_FILE = Path(__file__).resolve().with_name("chat_client.ui")


class SignalBridge(QtCore.QObject):
    """Cac signal giup cap nhat GUI an toan tu thread nen."""

    message_received = QtCore.pyqtSignal(str)
    status_changed = QtCore.pyqtSignal(str)
    connected_changed = QtCore.pyqtSignal(bool)


class ChatClientWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(str(UI_FILE), self)

        self.client_socket = None
        self.running = True
        self.socket_lock = threading.Lock()

        self.signals = SignalBridge()
        self.signals.message_received.connect(self.append_message)
        self.signals.status_changed.connect(self.lblStatus.setText)
        self.signals.connected_changed.connect(self.update_connection_state)

        self.txtServerHost.setText(DEFAULT_HOST)
        self.btnSend.setEnabled(False)

        self.btnConnect.clicked.connect(self.connect_to_server)
        self.btnSend.clicked.connect(self.send_message)
        self.txtMessage.returnPressed.connect(self.send_message)

    def connect_to_server(self):
        """Ket noi den server bang dia chi IP nguoi dung nhap."""
        host = self.txtServerHost.text().strip() or DEFAULT_HOST

        if self.client_socket is not None:
            self.append_message("[He thong] Client da ket noi den server.")
            return

        client_socket = None

        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.settimeout(5)
            client_socket.connect((host, PORT))
            client_socket.settimeout(None)
        except OSError as error:
            if client_socket is not None:
                try:
                    client_socket.close()
                except OSError:
                    pass
            self.signals.status_changed.emit("Trang thai: Khong ket noi duoc den server.")
            self.append_message(f"[Loi] Ket noi that bai den {host}:{PORT} - {error}")
            return

        with self.socket_lock:
            self.client_socket = client_socket

        self.signals.status_changed.emit(f"Trang thai: Da ket noi den {host}:{PORT}")
        self.signals.connected_changed.emit(True)
        self.append_message(f"[He thong] Da ket noi den server {host}:{PORT}.")

        threading.Thread(target=self.receive_messages, args=(client_socket,), daemon=True).start()

    def receive_messages(self, client_socket):
        """Nhan tin nhan tu server trong thread nen."""
        buffer = ""

        try:
            while self.running:
                data = client_socket.recv(BUFFER_SIZE)
                if not data:
                    break

                buffer += data.decode("utf-8")

                while "\n" in buffer:
                    message, buffer = buffer.split("\n", 1)
                    message = message.strip()
                    if message:
                        self.signals.message_received.emit(f"Server: {message}")
        except OSError as error:
            if self.running:
                self.signals.message_received.emit(f"[Loi] Mat ket noi voi server: {error}")
        finally:
            self.disconnect_from_server()

    def send_message(self):
        """Gui tin nhan den server."""
        message = self.txtMessage.text().strip()
        if not message:
            return

        with self.socket_lock:
            client_socket = self.client_socket

        if client_socket is None:
            self.append_message("[He thong] Chua ket noi den server.")
            return

        try:
            client_socket.sendall((message + "\n").encode("utf-8"))
            self.append_message(f"Client: {message}")
            self.txtMessage.clear()
        except OSError as error:
            self.append_message(f"[Loi] Khong gui duoc tin nhan: {error}")
            self.disconnect_from_server()

    def update_connection_state(self, connected):
        """Bat/tat cac dieu khien phu hop voi trang thai ket noi."""
        self.btnSend.setEnabled(connected)
        self.btnConnect.setEnabled(not connected)
        self.txtServerHost.setEnabled(not connected)

    def append_message(self, message):
        """Them noi dung vao khung chat."""
        self.txtMessages.append(message)

    def disconnect_from_server(self):
        """Dong socket client va cap nhat lai giao dien."""
        with self.socket_lock:
            client_socket = self.client_socket
            self.client_socket = None

        if client_socket is None:
            return

        try:
            client_socket.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass

        try:
            client_socket.close()
        except OSError:
            pass

        self.signals.connected_changed.emit(False)

        if self.running:
            self.signals.status_changed.emit("Trang thai: Da mat ket noi den server.")
            self.signals.message_received.emit("[He thong] Ket noi da dong.")
        else:
            self.signals.status_changed.emit("Trang thai: Client da dung.")

    def closeEvent(self, event):
        """Dong socket khi cua so bi tat."""
        self.running = False
        self.disconnect_from_server()
        event.accept()


def main():
    app = QtWidgets.QApplication([])
    window = ChatClientWindow()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
