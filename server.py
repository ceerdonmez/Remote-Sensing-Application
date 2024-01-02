import socket
import threading

def server():
    host = '127.0.0.1'
    port = 7000

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()

        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            threading.Thread(target=handle_client, args=(conn,)).start()

def handle_client(conn):
    while True:
        data = conn.recv(1024).decode()
        if not data:
            break

        print(data)  # Process and store data accordingly

if __name__ == "__main__":
    server()
