import socket
import threading

def handle_client(client_socket, address):
    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            if message:
                print(f"Received message from {address}: {message}")
                # Add your server logic here
        except ConnectionResetError:
            print(f"Connection with {address} closed.")
            client_socket.close()
            break

def main():
    host = '127.0.0.1'
    port = 8000
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)

    print(f"Server is listening on {host}:{port}")

    while True:
        client_socket, address = server.accept()
        print(f"Connection established with {address}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket, address))
        client_handler.start()

if __name__ == "__main__":
    main()