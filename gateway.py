import socket
import threading
import time

temperature_host = socket.gethostbyname(socket.gethostname())
temperature_port = 6000
temperature_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
temperature_socket.bind((temperature_host, temperature_port))  


humidity_host = socket.gethostbyname(socket.gethostname())
humidity_port = 6000
humidity_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
humidity_socket.bind((humidity_host, humidity_port))

server_host = socket.gethostbyname(socket.gethostname())
server_port = 7000

gateway_host = socket.gethostbyname(socket.gethostname())
gateway_port = 6001
def gateway():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as gateway_socket:
        gateway_socket.bind((gateway_host, gateway_port))
        print("Gateway is listening on port", gateway_port)
        gateway_socket.listen() 
        
        while True:
            conn, addr = gateway_socket.accept()
            print(conn)
            print("Im here1")
            with conn:
                print('Connected by', addr)
                threading.Thread(target=handle_client, args=(conn, temperature_socket, humidity_socket)).start()

def handle_client(client_socket, temperature_socket, humidity_socket):
    while True:
        data = client_socket.recv(1024).decode()
        print(data)
        if data.startswith('TEMPERATURE'):
            if not data:
                break
            try:
                temperature_socket.sendall(data.encode())
                print(data)
            except socket.error as e:
                print(f"Error sending data: {e}")
                time.sleep(2)  # or handle error in another appropriate way
        elif data.startswith('HUMIDITY'):
            try:
                humidity_socket.sendto(data.encode(), (server_host, server_port))
                print(data)
            except socket.error as e:
                print(f"Error sending data: {e}")
                time.sleep(2)  # or handle error in another appropriate way
if __name__ == "__main__":
    gateway()
