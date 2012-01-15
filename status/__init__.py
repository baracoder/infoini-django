import socket
import json

def get_all():
    HOST, PORT = "localhost", 0xCAFE

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((HOST, PORT))
        received = sock.recv(1024)
    finally:
        sock.close()
    return json.loads(received)

def ist_offen():
    return get_all()['tuer_offen']
