import socket
import time
import random


def temperature_sensor():
    host = socket.gethostbyname(socket.gethostname())
    port = 6001

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        while True:
            try:
                temperature_value = random.uniform(20, 30)
                timestamp = time.strftime("%m.%d.%Y:%H:%M:%S") # Get current time
                message = f'TEMPERATURE|{temperature_value}|{timestamp}'
                s.sendall(message.encode())
                print(message)
                time.sleep(1)
            except socket.error as e:
                print(f"Error receiving data: {e}")
                time.sleep(2)  # or handle error in another appropriate way

if __name__ == "__main__":
    temperature_sensor()
if __name__ == "__main__":
    temperature_sensor()
