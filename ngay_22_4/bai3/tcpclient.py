"""
Bai 3 - TCP Client gui danh sach mat khau de kiem tra

Chay file:
    python tcpclient.py
"""

import json
import socket


HOST = "127.0.0.1"  # Doi thanh IP may server neu can
PORT = 8092
BUFFER_SIZE = 1024


def send_json(connection, payload):
    """Gui du lieu JSON cho server."""
    message = json.dumps(payload, ensure_ascii=False) + "\n"
    connection.sendall(message.encode("utf-8"))


def receive_json(connection):
    """Nhan mot dong JSON tu server."""
    buffer = ""

    while "\n" not in buffer:
        data = connection.recv(BUFFER_SIZE)
        if not data:
            break
        buffer += data.decode("utf-8")

    if not buffer:
        raise ConnectionError("Server khong tra ve du lieu.")

    line = buffer.split("\n", 1)[0]
    return json.loads(line)


def input_passwords():
    """Nhap nhieu mat khau, tach boi dau phay va loai bo khoang trang thua."""
    while True:
        raw_text = input("Nhap cac mat khau, cach nhau boi dau phay: ").strip()

        passwords = [item.strip() for item in raw_text.split(",") if item.strip()]
        if passwords:
            return passwords

        print("Ban phai nhap it nhat 1 mat khau hop le ve mat dinh dang dau vao.")


def main():
    passwords = input_passwords()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))

        send_json(client_socket, {"passwords": passwords})
        print("[GUI] Da gui danh sach mat khau len server.")

        response = receive_json(client_socket)

        if not response.get("ok"):
            print(f"[LOI] {response.get('error', 'Khong xac dinh duoc loi.')}")
            return

        valid_passwords = response.get("valid_passwords", [])

        if valid_passwords:
            print("[KET QUA] Cac mat khau hop le:")
            print(", ".join(valid_passwords))
        else:
            print("[KET QUA] Khong co mat khau nao hop le.")


if __name__ == "__main__":
    main()
