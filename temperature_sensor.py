import socket
import threading
import time
import random
from logger import log_message as log

def main():
    host = "127.0.0.1"
    port = 9999

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client.connect((host, port))
    log("logs/temperature_logs.txt", f"Connected to {host}:{port}")

    while True:
        try:
            temperature_value = random.uniform(20, 30).__round__(
                2
            )  # Generate random temperature value
            timestamp = time.strftime("%m.%d.%Y:%H:%M:%S")  # Get current time
            message = f"TEMPERATURE|{temperature_value}|{timestamp}"
            log("logs/temperature_logs.txt", message)
            client.sendall(message.encode())
            print(message)
            time.sleep(1)
        except socket.error as e:
            print(f"Error receiving data: {e}")
            log("logs/temperature_logs.txt", f"Error receiving data: {e}")
            time.sleep(2)  # or handle error in another appropriate way


if __name__ == "__main__":
    main()
