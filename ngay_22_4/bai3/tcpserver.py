"""
Bai 3 - TCP Server kiem tra mat khau

Chay file:
    python tcpserver.py
"""

import json
import socket
import threading


HOST = "0.0.0.0"
PORT = 8092
BUFFER_SIZE = 1024
SPECIAL_CHARS = "$#@"


def send_json(connection, payload):
    """Gui du lieu JSON cho client."""
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


def is_valid_password(password):
    """Kiem tra mat khau theo 6 tieu chi de bai."""
    return (
        6 <= len(password) <= 12
        and any(char.islower() for char in password)
        and any(char.isupper() for char in password)
        and any(char.isdigit() for char in password)
        and any(char in SPECIAL_CHARS for char in password)
    )


def handle_client(client_socket, client_address):
    """Nhan danh sach mat khau, loc mat khau hop le va gui ket qua."""
    print(f"[KET NOI] Client {client_address} da ket noi.")

    try:
        payload = receive_json(client_socket)
        passwords = payload.get("passwords")

        if not isinstance(passwords, list):
            raise ValueError("Truong 'passwords' phai la mot danh sach.")

        valid_passwords = [
            password
            for password in passwords
            if isinstance(password, str) and is_valid_password(password)
        ]

        print(f"[XU LY] {client_address}: {len(valid_passwords)} mat khau hop le.")
        send_json(client_socket, {"ok": True, "valid_passwords": valid_passwords})
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
