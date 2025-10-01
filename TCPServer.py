import socket



def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))  # Bind to localhost on port 12345
    server_socket.listen(1)
    print("Server is listening...")
    ClientName = 0
    while True:
        ClientName +=1

        if ClientName <= 3:
            
            client_socket, addr = server_socket.accept()
            print(f"Client{ClientName:02d} Connection from {addr}")

            data = client_socket.recv(1024).decode()
            if data:
                print(f"Received: {data}")
                upcased_data = data.upper()
                client_socket.send(upcased_data.encode())

            client_socket.close()
        client_socket.close()

if __name__ == '__main__':
    start_server()
