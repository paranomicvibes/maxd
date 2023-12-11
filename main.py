import socket
from cryptography.fernet import Fernet

def read_server_details():
    with open('server_details.txt', 'r') as details_file:
        details = details_file.readlines()
        encryption_key_hex = details[1].split(":")[1].strip()
        encryption_key = bytes.fromhex(encryption_key_hex)
        return encryption_key

def encrypt_command(command, encryption_key):
    cipher_suite = Fernet(encryption_key)
    encrypted_command = cipher_suite.encrypt(command.encode('utf-8'))
    return encrypted_command

def decrypt_response(encrypted_response, encryption_key):
    cipher_suite = Fernet(encryption_key)
    decrypted_response = cipher_suite.decrypt(encrypted_response)
    return decrypted_response.decode('utf-8')

def main():
    encryption_key = read_server_details()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 8234))
    server_socket.listen(1)
    print("Server listening on port 8234...")

    client_socket, client_address = server_socket.accept()
    print(f"Connection established with {client_address}")

    while True:
        command_to_send = input("Enter command to send to the client: ")
        encrypted_command = encrypt_command(command_to_send, encryption_key)
        client_socket.send(encrypted_command)

        # Receive and decrypt the response from the client
        encrypted_response = client_socket.recv(4096)
        decrypted_response = decrypt_response(encrypted_response, encryption_key)
        print(f"Received response from client: {decrypted_response}")

    client_socket.close()
    server_socket.close()

if __name__ == "__main__":
    main()
