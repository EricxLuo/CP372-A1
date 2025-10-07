import socket
import os


SAVED_DIR = "downloaded"
os.makedirs(SAVED_DIR, exist_ok=True)
def start_client():

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))  # Connect to the server

    message = input("Enter your name to the server: ")
    client_socket.send(message.encode())

    registration_response = client_socket.recv(1024).decode()
    print(f"Server response: {registration_response}")

    while True:
        message = input("Enter a message or type 'status', 'list', 'get', or 'exit' to quit: ")

        if message.lower() == 'exit':
            break  # Exit the loop and close the connection

        client_socket.send(message.encode())  # Send the message to the server


        if message.lower() == "get":
            file_handle = None
            current_file = None
            while True:
                chunk = client_socket.recv(1024)
                if not chunk:
                    break

                text = chunk.decode(errors='ignore')
                lines = text.split("\n")

                i = 0
                while i < len(lines):
                    line = lines[i]

                    if line.startswith("START "):
                        filename = line.replace("START ", "").strip()
                        current_file = os.path.join(SAVED_DIR, filename)
                        file_handle = open(current_file, "wb")
                        print(f"Receiving file: {filename}")
                        rest = "\n".join(lines[i+1:]).encode()
                        if rest:
                            file_handle.write(rest)
                        break  
                    elif line.strip() == "END":
                        if file_handle:
                            file_handle.close()
                            file_handle = None
                            print(f"Finished file: {current_file}")
                    elif line.strip() == "ALL FILES SENT":
                        if file_handle:
                            file_handle.close()
                        print("All files received.")
                        break
                    else:
                        if file_handle:
                            file_handle.write((line + "\n").encode())
                    i += 1

                if b"ALL FILES SENT" in chunk:
                    break





        # Receive and print response from
        #  the server
        else:
            data = client_socket.recv(1024).decode()
            print(f"Received from server: {data}")

    
    client_socket.close()
    print("Connection closed.")

if __name__ == '__main__':
    start_client()

