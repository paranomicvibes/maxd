import os
import subprocess
from cryptography.fernet import Fernet

ACTIVATED_CLIENTS_FILE = 'activated_clients.txt'
CLIENT_TEMPLATE = 'cts.py'
CLIENTS_FOLDER = 'clients'

def generate_encryption_key():
    key = Fernet.generate_key()
    return key

def read_server_details():
    if os.path.exists('server_details.txt'):
        with open('server_details.txt', 'r') as details_file:
            details = details_file.readlines()
            encryption_key_hex = details[1].split(":")[1].strip()
            server_ip = details[0].split(":")[1].strip()
            encryption_key = bytes.fromhex(encryption_key_hex)
            return server_ip, encryption_key
    else:
        print("Error: Server details file not found.")
        return None, None

def generate_client_script(uid, server_ip, encryption_key):
    try:
        with open(CLIENT_TEMPLATE, 'r') as template_file:
            template_content = template_file.read()

            # Replace placeholders in the template with actual details
            template_content = template_content.replace('<UID>', uid)
            template_content = template_content.replace('<SERVER_IP>', server_ip)
            template_content = template_content.replace('<ENCRYPTION_KEY>', encryption_key.hex())

            # Create a folder for the client if it doesn't exist
            client_folder_path = os.path.join(CLIENTS_FOLDER, uid)
            os.makedirs(client_folder_path, exist_ok=True)

            # Save the generated client script in the client's folder
            client_script_path = os.path.join(client_folder_path, f'{uid}.py')
            with open(client_script_path, 'w') as client_script_file:
                client_script_file.write(template_content)

            # Log the activation in the activated clients file
            with open(ACTIVATED_CLIENTS_FILE, 'a') as activated_clients_file:
                activated_clients_file.write(f'{uid}\n')

            print(f"Client script for UID {uid} generated successfully.")
            print(f"Client script saved at: {client_script_path}")
    except Exception as e:
        print(f"Error generating client script: {e}")

def main():
    server_ip, encryption_key = read_server_details()

    if server_ip is not None and encryption_key is not None:
        uid = input("Enter a unique ID for the new client script: ")
        if uid not in open(ACTIVATED_CLIENTS_FILE).read():
            generate_client_script(uid, server_ip, encryption_key)
        else:
            print(f"Error: UID {uid} is already in use.")

if __name__ == "__main__":
    main()￼Enter
