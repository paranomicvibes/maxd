import socket

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 8234))
    server_socket.listen(1)
    print("Server listening on port 8234...")

    client_socket, client_address = server_socket.accept()
    print(f"Connection established with {client_address}")

    while True:
        command_to_send = input("Enter command to send to the client: ")
        client_socket.send(command_to_send.encode())

        # Receive and display the response from the client
        response = client_socket.recv(4096)
        print(f"Received response from client: {response.decode()}")

    client_socket.close()
    server_socket.close()

if __name__ == "__main__":
    main()