import socket
import struct
import json
import base64
import hmac
import hashlib
from typing import Any

HOST = '127.0.0.1'
PORT = 65433
SHARED_SECRET = b'supersecret'


def _recv_all(conn, n):
    data = b''
    while len(data) < n:
        packet = conn.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data


def recv_msg(conn):
    hdr = _recv_all(conn, 4)
    if not hdr:
        return None
    (length,) = struct.unpack('!I', hdr)
    body = _recv_all(conn, length)
    if body is None:
        return None
    return json.loads(body.decode())


def send_msg(conn, obj: Any):
    body = json.dumps(obj).encode()
    conn.sendall(struct.pack('!I', len(body)) + body)


class AuthClient:
    def __init__(self, host=HOST, port=PORT):
        self.host = host
        self.port = port
        self.sock = None

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        # チャレンジ受け取り
        chal = recv_msg(self.sock)
        if not chal or chal.get('type') != 'challenge':
            raise RuntimeError('no challenge')
        nonce = base64.b64decode(chal['nonce'].encode())
        sig = hmac.new(SHARED_SECRET, nonce, hashlib.sha256).digest()
        send_msg(self.sock, {'type': 'auth', 'hmac': sig.hex()})
        resp = recv_msg(self.sock)
        if not resp or resp.get('type') != 'ok':
            raise RuntimeError('auth failed')
        return True

    def close(self):
        if self.sock:
            self.sock.close()
            self.sock = None

    def cmd(self, name: str, **kwargs):
        send_msg(self.sock, {'type': 'cmd', 'cmd': name, **kwargs})
        return recv_msg(self.sock)


if __name__ == '__main__':
    c = AuthClient()
    c.connect()
    print(c.cmd('ping'))
    print(c.cmd('time'))
    print(c.cmd('echo', data='hello'))
    c.close()
