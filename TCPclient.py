import socket

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))  # Connect to the server

    message = input("Enter your name to the server: ")
    client_socket.send(message.encode())

    registration_response = client_socket.recv(1024).decode()
    print(f"Server response: {registration_response}")

    while True:
        message = input("Enter a message or type 'status' to see the server cache (type 'exit' to quit): ")

        if message.lower() == 'exit':
            break  # Exit the loop and close the connection

        client_socket.send(message.encode())  # Send the message to the server

        # Receive and print response from the server
        data = client_socket.recv(1024).decode()
        print(f"Received from server: {data}")

    
    client_socket.close()
    print("Connection closed.")

if __name__ == '__main__':
    start_client()

