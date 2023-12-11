import os
import subprocess
from cryptography.fernet import Fernet

DETAILS_FILE_PATH = 'server_details.txt'
SERVER_SCRIPT_PATH = 'main.py'  # Updated server script name

def generate_encryption_key():
    key = Fernet.generate_key()
    return key

def get_local_ip():
    try:
        result = subprocess.run(['ifconfig'], stdout=subprocess.PIPE, text=True)
        ip_lines = [line for line in result.stdout.split('\n') if 'IPv4 Address' in line]
        if ip_lines:
            local_ip = ip_lines[0].split(':')[-1].strip()
            return local_ip
    except Exception as e:
        print(f"Error getting local IP: {e}")
    return None

def read_or_generate_server_details():
    local_ip = get_local_ip()

    if local_ip is not None:
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
        print("Error: Unable to determine local IP.")
        return None, None

def run_server_script():
    try:
        subprocess.run(['python', SERVER_SCRIPT_PATH])
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
