import socket
import threading
import datetime

client_cache = {}


def handle_client(client_socket, client_id):
    connected_time = datetime.datetime.now()
    client_cache[client_id] = {"NAME": None, "Connect": connected_time, "Disconnect": None}

    try:
        while True:

            data = client_socket.recv(1024).decode()

            if not data:
                break

            if client_cache[client_id]["NAME"] is None:
                client_cache[client_id]["Name"] = data
                print(f"Client {client_id} registered as {data}")
                client_socket.send("Name registered".encode())

            elif data.lower() == 'status':
                cache_info = "\n".join([
                    f"Client {cid}: Name={info['Name']}, Connect={info['Connect']}, Disconnect={info['Disconnect']}"
                    for cid, info in client_cache.items()
                ])
                client_socket.send(f"Server Cache:\n{cache_info}".encode())

            else:
                print(f"Received: {data}")
                upcased_data = data.upper()
                client_socket.send(upcased_data.encode())

               

    finally:
        client_cache[client_id]["Disconnect"] = datetime.datetime.now()
        client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))  # Bind to localhost on port 12345
    server_socket.listen(1)
    print("Server is listening...")
    ClientName = 0
    while True:
        ClientName += 1
        if ClientName <= 3:
            
            client_socket, client_id = server_socket.accept()
            print(f"Client{ClientName:02d} Connection from {client_id}")

            # Corrected thread creation
            client_handler = threading.Thread(target=handle_client, args=(client_socket, client_id))
            client_handler.start()

        else:
            break 

if __name__ == '__main__':
    start_server()
