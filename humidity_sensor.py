import socket
import time
import random

def humidity_sensor():
    host = '127.0.0.1'
    port = 6000

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        while True:
            humidity_value = random.uniform(40, 90)
            if humidity_value > 80:
                message = f'HUMIDITY|{humidity_value}'
                s.sendto(message.encode(), (host, port))
            time.sleep(1)

            if time.time() % 3 == 0:
                alive_message = 'ALIVE'
                s.sendto(alive_message.encode(), (host, port))
                time.sleep(1)

if __name__ == "__main__":
    humidity_sensor()
