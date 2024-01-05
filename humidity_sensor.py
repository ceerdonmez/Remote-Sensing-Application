import socket
import threading
import time
import random


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
                message = f"HUMIDITY|{humidity_value}"
                client.sendto(message.encode(), (host, port))
                print(message)
            time.sleep(1)
            if int(time.time()) % 3 == 0:
                alive_message = "ALIVE"
                client.sendto(alive_message.encode(), (host, port))

                time.sleep(1)
        except socket.error as e:
            print(f"Error receiving data: {e}")
            time.sleep(2)  # or handle error in another appropriate way


if __name__ == "__main__":
    main()
