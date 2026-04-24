"""
Bai 2 - TCP Client nhap 2 so nguyen va nhan tong

Chay file:
    python tcpclient.py
"""

import json
import socket


HOST = "127.0.0.1"  # Doi thanh IP may server neu can
PORT = 8091
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


def input_integer(prompt):
    """Nhap du lieu tu ban phim cho den khi dung so nguyen."""
    while True:
        value = input(prompt).strip()
        try:
            return int(value)
        except ValueError:
            print("Gia tri khong hop le. Vui long nhap mot so nguyen.")


def main():
    a = input_integer("Nhap so nguyen a: ")
    b = input_integer("Nhap so nguyen b: ")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))

        send_json(client_socket, {"a": a, "b": b})
        print(f"[GUI] Da gui a = {a}, b = {b} len server.")

        response = receive_json(client_socket)

        if response.get("ok"):
            print(f"[KET QUA] Tong a + b = {response['result']}")
        else:
            print(f"[LOI] {response.get('error', 'Khong xac dinh duoc loi.')}")


if __name__ == "__main__":
    main()
