"""
Bai 1 - TCP Server

Chay file:
    python tcpserver.py
"""

import socket
import threading


HOST = "0.0.0.0"  # Lang nghe tren moi dia chi mang cua may server
PORT = 8090
BUFFER_SIZE = 1024
SERVER_MESSAGE = "From SERVER TCP"


def handle_client(client_socket, client_address):
    """Xu ly tung client trong mot luong rieng."""
    print(f"[KET NOI] Client {client_address} da ket noi.")

    try:
        data = client_socket.recv(BUFFER_SIZE)
        if not data:
            print(f"[THONG BAO] Client {client_address} khong gui du lieu.")
            return

        message = data.decode("utf-8").strip()
        print(f"[NHAN] Tu {client_address}: {message}")

        client_socket.sendall(SERVER_MESSAGE.encode("utf-8"))
        print(f"[GUI] Den {client_address}: {SERVER_MESSAGE}")
    except UnicodeDecodeError:
        print(f"[LOI] Du lieu tu {client_address} khong dung dinh dang UTF-8.")
    except OSError as error:
        print(f"[LOI] Loi ket noi voi {client_address}: {error}")
    finally:
        client_socket.close()
        print(f"[DONG] Da dong ket noi voi {client_address}.")


def main():
    """Khoi tao TCP server va cho phep nhieu client ket noi dong thoi."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        # Cho phep tai su dung cong sau khi server duoc khoi dong lai.
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen()

        print(f"TCP Server dang lang nghe tai {HOST}:{PORT}")
        print("Nhan Ctrl+C de dung server.\n")

        try:
            while True:
                client_socket, client_address = server_socket.accept()

                # Moi client duoc xu ly boi mot thread rieng de ho tro nhieu ket noi.
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
