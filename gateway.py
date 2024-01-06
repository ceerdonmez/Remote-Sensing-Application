import socket
import threading
import time
from logger import log_message as log
import random

server_host = "127.0.0.1"
server_port = 8082


def handshake():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server_host, server_port))

    server_msg = sock.recv(1024)
    print(f"Received from server: {server_msg.decode()}")
    log("logs/gateway_logs.txt", f"Received from server: {server_msg.decode()}")
    # Send response to server
    if server_msg:
        sock.send(b"ACK")
        print("Sent ACK to server for handshake")

        # Receive acknowledgment from server after handshake
        ack_response = sock.recv(1024)
        print(f"Server response after handshake: {ack_response.decode()}")
        log(
            "logs/gateway_logs.txt",
            f"Server response after handshake: {ack_response.decode()}",
        )

        start_gateway()
    else:
        print("Server did not respond to handshake")
        log("logs/gateway_logs.txt", "Server did not respond to handshake")
        sock.close()


# Function to handle each client connection
def handle_tcp_client(client_socket, address):
    global last_message_time
    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")

            if message:
                print(f"Received message from {address}: {message}")
                log(
                    "logs/gateway_logs.txt",
                    f"Received message from {address}: {message}",
                )
                broadcast(message)
                last_message_time = time.time()
            if (int(time.time()) - int(last_message_time)) > 10:
                print("'TEMP SENSOR OFF'")
                log("logs/gateway_logs.txt", "'TEMP SENSOR OFF'")
                broadcast("'TEMP SENSOR OFF'")
                client_socket.close()
                break

        except ConnectionResetError:
            print(f"Connection with {address} closed.")
            log("logs/gateway_logs.txt", f"Connection with {address} closed.")
            client_socket.close()
            break


def handle_udp_client(udp_gateway):

    while True:
        try:

            message, address = udp_gateway.recvfrom(1024)
            udp_gateway.settimeout(7.0)
            if message:
                print(f"Received message from {address}: {message}")
                log(
                    "logs/gateway_logs.txt",
                    f"Received message from {address}: {message}",
                )
                broadcast(message.decode("utf-8"))

        except ConnectionResetError:
            log("logs/gateway_logs.txt", f"Connection with {address} closed.")
            udp_gateway.close()
            break
        except socket.timeout:
            broadcast("'HUMIDITY SENSOR OFF'")
            print("HUMIDITY SENSOR OFF")
            log("logs/gateway_logs.txt", "HUMIDITY SENSOR OFF")

            break


# Function to broadcast message to all clients except the sender
def broadcast(message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.connect((server_host, server_port))

    sock.sendall(message.encode("utf-8"))
    print(f"Sent message to {server_host}:{server_port}: {message}")
    log(
        "logs/gateway_logs.txt",
        f"Sent message to {server_host}:{server_port}: {message}",
    )
    sock.close()


def start_gateway():
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

    log(
        "logs/gateway_logs.txt",
        f"Gateway is listening for TCP connections on {host}:{tcp_port}",
    )
    log(
        "logs/gateway_logs.txt",
        f"Gateway is listening for UDP messages on {host}:{udp_port}",
    )

    udp_thread = threading.Thread(target=handle_udp_client, args=(udp_gateway,))
    udp_thread.start()

    while True:
        # Accept TCP client connection
        tcp_client_socket, address = tcp_gateway.accept()
        print(f"Connection established with {address}")
        log("logs/gateway_logs.txt", f"Connection established with {address}")
        # Handle TCP client connection in a separate thread
        tcp_client_handler = threading.Thread(
            target=handle_tcp_client, args=(tcp_client_socket, address)
        )
        tcp_client_handler.start()


if __name__ == "__main__":
    handshake()
