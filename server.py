import socket
import threading
import sqlite3
import pandas as pd
from logger import log_message as log


conn = sqlite3.connect("sensor_data.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS temp_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        temperature FLOAT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP

    )
"""
)
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS humidity_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        humidity FLOAT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP

    )
"""
)
host = "127.0.0.1"
port = 8082

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(5)


def handle_client(client_socket, address):
    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            if message:
                print(f"Received message from {address}: {message}")
                log(
                    "logs/server_logs.txt",
                    f"Received message from {address}: {message}",
                )
                if message.startswith("TEMPERATURE"):
                    cursor.execute(
                        """ 
                        INSERT INTO temp_data (temperature,timestamp) VALUES (?,?)
                    """,
                        (float(message.split("|")[1]), message.split("|")[2]),
                    )
                    conn.commit()
                    log(
                        "logs/server_logs.txt",
                        f"Temperature data inserted into database",
                    )

                elif message.startswith("HUMIDITY"):
                    cursor.execute(
                        """ 
                        INSERT INTO humidity_data (humidity,timestamp) VALUES (?,?)
                    """,
                        (float(message.split("|")[1]), message.split("|")[2]),
                    )
                    conn.commit()
                    log("logs/server_logs.txt", f"Humidity data inserted into database")

        except ConnectionResetError:

            client_socket.close()
            break


def get_temperature():

    data = pd.read_sql_query("SELECT * FROM temp_data", conn)
    return data


def get_humidity():
    data = pd.read_sql_query("SELECT * FROM humidity_data", conn)
    return data


def get_last_humidity():
    data = pd.read_sql_query(
        "SELECT * FROM humidity_data ORDER BY id DESC LIMIT 1", conn
    )
    return data


def start_server():

    print(f"Server is listening on {host}:{port}")
    log("logs/server_logs.txt", f"Server is listening on {host}:{port}")

    while True:
        client_socket, address = server.accept()

        client_handler = threading.Thread(
            target=handle_client, args=(client_socket, address)
        )
        client_handler.start()


def handshake():
    print("Server is waiting for a connection...")
    conn, addr = server.accept()
    print(f"Connection established with {addr}")

    # Perform handshake
    conn.send(b"Handshake initiated. Waiting for client response...")
    client_response = conn.recv(1024)
    print(f"Received from client: {client_response.decode()}")

    # If handshake is successful, proceed with further communication
    if client_response.decode() == "ACK":
        conn.send(b"Handshake successful. Starting server...")
        log("logs/server_logs.txt", "Handshake successful. Starting server...")
        start_server()
    else:
        conn.send(b"Handshake unsuccessful. Closing connection...")
        log("logs/server_logs.txt", "Handshake unsuccessful. Closing connection...")
        conn.close()


if __name__ == "__main__":
    handshake()
