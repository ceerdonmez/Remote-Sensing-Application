import socket
import time
import random

def temperature_sensor():
    host = '127.0.0.1'
    port = 5000

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        while True:
            temperature_value = random.uniform(20, 30)
            timestamp = time.time()
            message = f'TEMPERATURE|{temperature_value}|{timestamp}'
            s.sendall(message.encode())
            time.sleep(1)

if __name__ == "__main__":
    temperature_sensor()
