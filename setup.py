import os
from cryptography.fernet import Fernet

DETAILS_FILE_PATH = 'server_details.txt'
SERVER_SCRIPT_PATH = 'main.py'

def generate_encryption_key():
    key = Fernet.generate_key()
    return key

def get_local_ip():
    local_ip = input("Enter the local IP address: ")
    return local_ip.strip()

def read_or_generate_server_details():
    local_ip = get_local_ip()

    if local_ip:
        if os.path.exists(DETAILS_FILE_PATH):
            with open(DETAILS_FILE_PATH, 'r') as details_file:
                details = details_file.readlines()
                encryption_key_hex = details[1].split(":")[1].strip()
                encryption_key = bytes.fromhex(encryption_key_hex)
                return local_ip, encryption_key
        else:
            encryption_key = generate_encryption_key()
            with open(DETAILS_FILE_PATH, 'w') as details_file:
                details_file.write(f"Local IP: {local_ip}\n")
                details_file.write(f"Encryption Key: {encryption_key.hex()}\n")
            return local_ip, encryption_key
    else:
        print("Error: Invalid local IP.")
        return None, None

def run_server_script():
    try:
        os.system(f'python {SERVER_SCRIPT_PATH}')
    except Exception as e:
        print(f"Error running server script: {e}")

def main():
    server_ip, encryption_key = read_or_generate_server_details()

    if server_ip is not None and encryption_key is not None:
        print(f"Local IP: {server_ip}")
        print(f"Encryption Key: {encryption_key.hex()}")

        run_server_script()

if __name__ == "__main__":
    main()
