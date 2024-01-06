import socket
import threading
import time
from logger import log_message as log

# Function to handle each client connection
def handle_tcp_client(client_socket, address):
    global last_message_time
    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
           
            if message:
                print(f"Received message from {address}: {message}")
                log("logs/gateway_logs.txt",f"Received message from {address}: {message}")
                broadcast(message)
                last_message_time = time.time()
            if (int(time.time()) - int(last_message_time)) > 10:
                print("'TEMP SENSOR OFF'")
                log("logs/gateway_logs.txt","'TEMP SENSOR OFF'")
                broadcast("'TEMP SENSOR OFF'")
                client_socket.close()
                break
            
            
        except ConnectionResetError:
            print(f"Connection with {address} closed.")
            log("logs/gateway_logs.txt",f"Connection with {address} closed.")
            client_socket.close()
            break

def handle_udp_client(udp_gateway):

    while True:
        try:
            message, address = udp_gateway.recvfrom(1024)
            if message:
                print(f"Received message from {address}: {message}")
                log("logs/gateway_logs.txt",f"Received message from {address}: {message}")
                broadcast(message.decode("utf-8"))           
        except ConnectionResetError:
            log("logs/gateway_logs.txt",f"Connection with {address} closed.")
            udp_gateway.close()
            break
        

# Function to broadcast message to all clients except the sender
def broadcast(message):
    server_host = "127.0.0.1"
    server_port = 8080

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect((server_host, server_port))
    server_socket.sendall(message.encode("utf-8"))
    print(f"Sent message to {server_host}:{server_port}: {message}")
    log("logs/gateway_logs.txt",f"Sent message to {server_host}:{server_port}: {message}")
    server_socket.close()


def main():
    host = "127.0.0.1"
    tcp_port = 9999
    udp_port = 8888

    tcp_gateway = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_gateway.bind((host, tcp_port))
    tcp_gateway.listen(5)

    udp_gateway = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_gateway.bind((host, udp_port))

    print(f"Gateway is listening for TCP connections on {host}:{tcp_port}")
    print(f"Gateway is listening for UDP messages on {host}:{udp_port}")

    log("logs/gateway_logs.txt",f"Gateway is listening for TCP connections on {host}:{tcp_port}")
    log("logs/gateway_logs.txt",f"Gateway is listening for UDP messages on {host}:{udp_port}")

    udp_thread = threading.Thread(target=handle_udp_client, args=(udp_gateway,))
    udp_thread.start()

    while True:
        # Accept TCP client connection
        tcp_client_socket, address = tcp_gateway.accept()
        print(f"Connection established with {address}")
        log("logs/gateway_logs.txt",f"Connection established with {address}")
        # Handle TCP client connection in a separate thread
        tcp_client_handler = threading.Thread(
            target=handle_tcp_client, args=(tcp_client_socket, address)
        )
        tcp_client_handler.start()


if __name__ == "__main__":
    main()
