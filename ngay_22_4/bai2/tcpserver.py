"""
Bai 2 - TCP Server tinh tong 2 so nguyen

Chay file:
    python tcpserver.py
"""

import json
import socket
import threading


HOST = "0.0.0.0"
PORT = 8091
BUFFER_SIZE = 1024


def send_json(connection, payload):
    """Gui du lieu JSON ket thuc bang ky tu xuong dong de tach goi tin."""
    message = json.dumps(payload, ensure_ascii=False) + "\n"
    connection.sendall(message.encode("utf-8"))


def receive_json(connection):
    """Nhan mot dong JSON tu client."""
    buffer = ""

    while "\n" not in buffer:
        data = connection.recv(BUFFER_SIZE)
        if not data:
            break
        buffer += data.decode("utf-8")

    if not buffer:
        raise ValueError("Khong nhan duoc du lieu tu client.")

    line = buffer.split("\n", 1)[0]

    try:
        return json.loads(line)
    except json.JSONDecodeError as error:
        raise ValueError("Du lieu gui len khong dung dinh dang JSON.") from error


def validate_numbers(payload):
    """Kiem tra payload co chua dung 2 so nguyen a va b hay khong."""
    if not isinstance(payload, dict):
        raise ValueError("Du lieu phai la mot doi tuong JSON.")

    if "a" not in payload or "b" not in payload:
        raise ValueError("Thieu gia tri a hoac b.")

    a = payload["a"]
    b = payload["b"]

    if not isinstance(a, int) or not isinstance(b, int):
        raise ValueError("a va b phai la so nguyen.")

    return a, b


def handle_client(client_socket, client_address):
    """Nhan du lieu, tinh tong va gui ket qua tra ve client."""
    print(f"[KET NOI] Client {client_address} da ket noi.")

    try:
        payload = receive_json(client_socket)
        a, b = validate_numbers(payload)

        total = a + b
        print(f"[TINH TOAN] {client_address}: {a} + {b} = {total}")

        send_json(client_socket, {"ok": True, "result": total})
    except ValueError as error:
        send_json(client_socket, {"ok": False, "error": str(error)})
        print(f"[LOI] {client_address}: {error}")
    except OSError as error:
        print(f"[LOI] Loi ket noi voi {client_address}: {error}")
    finally:
        client_socket.close()
        print(f"[DONG] Da dong ket noi voi {client_address}.")


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen()

        print(f"TCP Server dang lang nghe tai {HOST}:{PORT}")
        print("Nhan Ctrl+C de dung server.\n")

        try:
            while True:
                client_socket, client_address = server_socket.accept()
                client_thread = threading.Thread(
                    target=handle_client,
                    args=(client_socket, client_address),
                    daemon=True,
                )
                client_thread.start()
        except KeyboardInterrupt:
            print("\n[THONG BAO] Server da dung.")


if __name__ == "__main__":
    main()
