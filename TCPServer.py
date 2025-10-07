import socket
import threading
import datetime
import os

client_cache = {}

DIR = "repository"

def handle_client(client_socket, client_id):
    connected_time = datetime.datetime.now()
    client_cache[client_id] = {"Name": None, "Connect": connected_time, "Disconnect": None}


    try:
        while True:
            data = client_socket.recv(1024).decode()
            if not data:
                break

            if client_cache[client_id]["Name"] is None:
                client_cache[client_id]["Name"] = data
                print(f"Client {client_id} registered as {data}")
                client_socket.send("Name registered".encode())
                continue

            if data.lower() == 'status':
                cache_info = "\n".join([
                    f"Client {cid}: Name={info['Name']}, Connect={info['Connect']}, Disconnect={info['Disconnect']}"
                    
                    for cid, info in client_cache.items()

                ])
                client_socket.send(f"Server Cache:\n{cache_info}".encode())


            elif data.lower()  == "list":
                files = os.listdir(DIR)
                if files:
                    file_list = "\n".join(files)
                    client_socket.send(f"Files in repository:\n{file_list}".encode())
                else:

                    client_socket.send("No files in repository.\n".encode())
                    
                
            elif data.lower() == "get":
                send_all_files(client_socket)

            else:
                print(f"Received from {client_cache[client_id]['Name']}: {data}")
                response = data + " ACK"
                client_socket.send(response.encode())

               

    finally:
        print(f"Client {client_cache[client_id]['Name']} disconnected")
        client_cache[client_id]["Disconnect"] = datetime.datetime.now()
        client_socket.close()

def send_all_files(client_socket):
    files = os.listdir(DIR)
    if not files:
        client_socket.send(b"No files available.\n")
        return

    for filename in files:
        file_path = os.path.join(DIR, filename)
        if not os.path.isfile(file_path):
            continue  # skip directories

        client_socket.send(f"START {filename}\n".encode())

        with open(file_path, 'rb') as f:

            while fileChunk := f.read(1024):
                client_socket.send(fileChunk)

        client_socket.send(b"\nEND\n")
    client_socket.send(b"ALL FILES SENT\n")
    print("FILES SENT")



def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))  
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
