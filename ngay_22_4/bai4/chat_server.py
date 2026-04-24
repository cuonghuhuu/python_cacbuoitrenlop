"""
Bai 4 - Chat Server GUI

Chay file:
    python chat_server.py
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


HOST = "0.0.0.0"
PORT = 8093
BUFFER_SIZE = 1024
UI_FILE = Path(__file__).resolve().with_name("chat_server.ui")


class SignalBridge(QtCore.QObject):
    """Cac signal giup cap nhat GUI an toan tu thread nen."""

    message_received = QtCore.pyqtSignal(str)
    status_changed = QtCore.pyqtSignal(str)
    send_enabled = QtCore.pyqtSignal(bool)


class ChatServerWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(str(UI_FILE), self)

        self.server_socket = None
        self.client_socket = None
        self.client_address = None
        self.running = True
        self.socket_lock = threading.Lock()

        self.signals = SignalBridge()
        self.signals.message_received.connect(self.append_message)
        self.signals.status_changed.connect(self.lblStatus.setText)
        self.signals.send_enabled.connect(self.btnSend.setEnabled)

        self.btnSend.clicked.connect(self.send_message)
        self.txtMessage.returnPressed.connect(self.send_message)
        self.btnSend.setEnabled(False)

        self.start_server()

    def start_server(self):
        """Mo socket server va bat dau lang nghe ket noi tu client."""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((HOST, PORT))
            self.server_socket.listen(1)
        except OSError as error:
            self.signals.status_changed.emit(f"Trang thai: Khong mo duoc server. {error}")
            self.append_message(f"[Loi] Khong the khoi tao server: {error}")
            return

        self.signals.status_changed.emit(
            f"Trang thai: Dang lang nghe tai cong {PORT}, cho client ket noi..."
        )
        self.append_message(f"[He thong] Server dang lang nghe tai {HOST}:{PORT}.")

        threading.Thread(target=self.accept_client_loop, daemon=True).start()

    def accept_client_loop(self):
        """Cho client ket noi. Server trong bai nay phuc vu 1 client tai 1 thoi diem."""
        while self.running and self.server_socket:
            try:
                client_socket, client_address = self.server_socket.accept()
            except OSError:
                break

            with self.socket_lock:
                has_client = self.client_socket is not None

            if has_client:
                try:
                    client_socket.sendall(
                        "Server dang phuc vu mot client khac.\n".encode("utf-8")
                    )
                except OSError:
                    pass
                client_socket.close()
                continue

            with self.socket_lock:
                self.client_socket = client_socket
                self.client_address = client_address

            self.signals.status_changed.emit(
                f"Trang thai: Da ket noi voi {client_address[0]}:{client_address[1]}"
            )
            self.signals.send_enabled.emit(True)
            self.signals.message_received.emit(
                f"[He thong] Client {client_address[0]}:{client_address[1]} da ket noi."
            )

            threading.Thread(
                target=self.receive_messages,
                args=(client_socket, client_address),
                daemon=True,
            ).start()

    def receive_messages(self, client_socket, client_address):
        """Nhan du lieu lien tuc tu client ma khong lam treo GUI."""
        buffer = ""

        try:
            while self.running:
                data = client_socket.recv(BUFFER_SIZE)
                if not data:
                    break

                buffer += data.decode("utf-8")

                # Tach tung tin nhan theo ky tu xuong dong.
                while "\n" in buffer:
                    message, buffer = buffer.split("\n", 1)
                    message = message.strip()
                    if message:
                        self.signals.message_received.emit(f"Client: {message}")
        except OSError as error:
            if self.running:
                self.signals.message_received.emit(
                    f"[Loi] Mat ket noi voi client {client_address}: {error}"
                )
        finally:
            self.disconnect_client()

    def send_message(self):
        """Gui tin nhan tu server den client."""
        message = self.txtMessage.text().strip()
        if not message:
            return

        with self.socket_lock:
            client_socket = self.client_socket

        if client_socket is None:
            self.append_message("[He thong] Chua co client nao dang ket noi.")
            return

        try:
            client_socket.sendall((message + "\n").encode("utf-8"))
            self.append_message(f"Server: {message}")
            self.txtMessage.clear()
        except OSError as error:
            self.append_message(f"[Loi] Khong gui duoc tin nhan: {error}")
            self.disconnect_client()

    def append_message(self, message):
        """Them noi dung vao o hien thi chat."""
        self.txtMessages.append(message)

    def disconnect_client(self):
        """Dong ket noi hien tai va dua giao dien ve trang thai cho."""
        with self.socket_lock:
            client_socket = self.client_socket
            client_address = self.client_address
            self.client_socket = None
            self.client_address = None

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

        self.signals.send_enabled.emit(False)

        if self.running:
            self.signals.status_changed.emit(
                f"Trang thai: Dang lang nghe tai cong {PORT}, cho client ket noi..."
            )
            self.signals.message_received.emit(
                f"[He thong] Client {client_address[0]}:{client_address[1]} da ngat ket noi."
            )
        else:
            self.signals.status_changed.emit("Trang thai: Server da dung.")

    def closeEvent(self, event):
        """Dong toan bo socket khi cua so bi tat."""
        self.running = False

        self.disconnect_client()

        if self.server_socket is not None:
            try:
                self.server_socket.close()
            except OSError:
                pass

        event.accept()


def main():
    app = QtWidgets.QApplication([])
    window = ChatServerWindow()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
