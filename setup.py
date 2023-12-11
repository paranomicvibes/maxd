import os

DETAILS_FILE_PATH = 'server_details.txt'
SERVER_SCRIPT_PATH = 'main.py'

def get_local_ip():
    local_ip = input("Enter the local IP address: ")
    return local_ip.strip()

def write_server_details(local_ip):
    with open(DETAILS_FILE_PATH, 'w') as details_file:
        details_file.write(f"Local IP: {local_ip}\n")

def run_server_script():
    try:
        os.system(f'python {SERVER_SCRIPT_PATH}')
    except Exception as e:
        print(f"Error running server script: {e}")

def main():
    local_ip = get_local_ip()

    if local_ip:
        write_server_details(local_ip)
        print(f"Local IP: {local_ip}")

        run_server_script()

if __name__ == "__main__":
    main()