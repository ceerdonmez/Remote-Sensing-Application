import socket
import threading
import time
import random


def main():
    host = "127.0.0.1"
    port = 9999

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client.connect((host, port))

    while True:
        try:
            temperature_value = random.uniform(20, 30).__round__(
                2
            )  # Generate random temperature value
            timestamp = time.strftime("%m.%d.%Y:%H:%M:%S")  # Get current time
            message = f"TEMPERATURE|{temperature_value}|{timestamp}"
            client.sendall(message.encode())
            print(message)
            time.sleep(1)
        except socket.error as e:
            print(f"Error receiving data: {e}")
            time.sleep(2)  # or handle error in another appropriate way


if __name__ == "__main__":
    main()
