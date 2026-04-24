"""
Bai 1 - TCP Client

Chay file:
    python tcpclient.py
"""

import socket


HOST = "127.0.0.1"  # Doi thanh IP may server neu chay tren 2 may khac nhau
PORT = 8090
BUFFER_SIZE = 1024
CLIENT_MESSAGE = "From CLIENT TCP"


def main():
    """Ket noi den server, gui chuoi va nhan phan hoi."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))

        print(f"[KET NOI] Da ket noi den server {HOST}:{PORT}")

        client_socket.sendall(CLIENT_MESSAGE.encode("utf-8"))
        print(f"[GUI] {CLIENT_MESSAGE}")

        response = client_socket.recv(BUFFER_SIZE).decode("utf-8").strip()
        print(f"[NHAN] {response}")


if __name__ == "__main__":
    main()
