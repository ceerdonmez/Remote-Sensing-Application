import socket
import threading
import time

def gateway():
    temperature_host = '127.0.0.1'
    temperature_port = 5000

    humidity_host = '127.0.0.1'
    humidity_port = 6000

    server_host = '127.0.0.1'
    server_port = 7000

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((server_host, server_port))
        server_socket.listen()

        temperature_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        temperature_socket.connect((temperature_host, temperature_port))

        humidity_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        humidity_socket.bind((humidity_host, humidity_port))

        while True:
            conn, addr = server_socket.accept()
            with conn:
                threading.Thread(target=handle_client, args=(conn, temperature_socket, humidity_socket)).start()

def handle_client(client_socket, temperature_socket, humidity_socket):
    while True:
        data = client_socket.recv(1024).decode()
        if not data:
            break

        if data.startswith('TEMPERATURE'):
            temperature_socket.sendall(data.encode())
        elif data.startswith('HUMIDITY'):
            humidity_socket.sendto(data.encode(), ('127.0.0.1', 6000))

if __name__ == "__main__":
    gateway()
