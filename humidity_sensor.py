import socket
import threading
import time
import random
from logger import log_message as log


def main():
    host = "127.0.0.1"
    port = 8888

    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True:
        try:
            humidity_value = random.uniform(40, 90).__round__(
                2
            )  # Generate random humidity value

            if humidity_value > 80:
                timestamp = time.strftime("%m.%d.%Y:%H:%M:%S")  # Get current time
                message = f"HUMIDITY|{humidity_value}|{timestamp}"
                client.sendto(message.encode(), (host, port))
                print(message)
                log("logs/humidity_logs.txt", message)
            time.sleep(1)
            if int(time.time()) % 3 == 0:
                alive_message = "ALIVE"
                client.sendto(alive_message.encode(), (host, port))
                print(alive_message)
                log("logs/humidity_logs.txt", alive_message)

                time.sleep(1)
        except socket.error as e:
            print(f"Error receiving data: {e}")
            log("logs/humidity_logs.txt", f"Error receiving data: {e}")
            time.sleep(2)  # or handle error in another appropriate way


if __name__ == "__main__":
    main()
