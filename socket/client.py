import socket
import sys

HOST = '127.0.0.1'
PORT = 65432


def run_client(message: str):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(message.encode())
        data = s.recv(1024)
    return data.decode()


if __name__ == '__main__':
    msg = ' '.join(sys.argv[1:]) if len(sys.argv) > 1 else 'Hello, socket world!'
    resp = run_client(msg)
    print('Received:', resp)
