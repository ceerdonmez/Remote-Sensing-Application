import socket
import threading


header = 64   
port = 7000
host =socket.gethostbyname(socket.gethostname())  # Get local machine name
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
format = 'utf-8'



def start():
    print(f"[LISTENING] Server is listening on {host}")
    server.listen()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client,args=(conn,addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
        


def handle_client(conn,addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        data = conn.recv(header).decode(format)
        if data:
            msg_length = len(data)
            msg = conn.recv(msg_length).decode(format)
            print(f"[{addr}] {msg}")
            conn.send("Message received".encode(format))
    conn.close()

if __name__ == "__main__":
    start()
