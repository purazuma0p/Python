import socket
import threading
import json
import struct
import hmac
import hashlib
import os
import time
import base64

HOST = '127.0.0.1'
PORT = 65433

# 共有シークレット（学習用）。実運用では安全に管理すること。
SHARED_SECRET = b'supersecret'

# 簡易的なファイルストレージ（メモリ）
_storage = {}
_storage_lock = threading.Lock()


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


def send_msg(conn, obj):
    body = json.dumps(obj).encode()
    conn.sendall(struct.pack('!I', len(body)) + body)


def handle_authenticated(conn, addr):
    try:
        # 認証チャレンジを送る
        challenge = os.urandom(16)
        send_msg(conn, {'type': 'challenge', 'nonce': base64.b64encode(challenge).decode()})

        # クライアントの応答を待つ
        msg = recv_msg(conn)
        if not msg or msg.get('type') != 'auth' or 'hmac' not in msg:
            send_msg(conn, {'type': 'error', 'message': 'auth required'})
            return

        recv_hmac = bytes.fromhex(msg['hmac'])
        expected = hmac.new(SHARED_SECRET, challenge, hashlib.sha256).digest()
        if not hmac.compare_digest(recv_hmac, expected):
            send_msg(conn, {'type': 'error', 'message': 'auth failed'})
            return

        send_msg(conn, {'type': 'ok', 'message': 'authenticated'})

        # 認証済みとしてコマンドループ
        while True:
            req = recv_msg(conn)
            if req is None:
                break
            if req.get('type') != 'cmd' or 'cmd' not in req:
                send_msg(conn, {'type': 'error', 'message': 'invalid request'})
                continue
            cmd = req['cmd']
            if cmd == 'ping':
                send_msg(conn, {'type': 'resp', 'result': 'pong'})
            elif cmd == 'time':
                send_msg(conn, {'type': 'resp', 'result': time.time()})
            elif cmd == 'echo':
                send_msg(conn, {'type': 'resp', 'result': req.get('data')})
            elif cmd == 'upload':
                filename = req.get('filename')
                data_b64 = req.get('data')
                if not filename or not data_b64:
                    send_msg(conn, {'type': 'error', 'message': 'upload needs filename and data'})
                    continue
                try:
                    data = base64.b64decode(data_b64.encode())
                except Exception:
                    send_msg(conn, {'type': 'error', 'message': 'invalid base64'})
                    continue
                if len(data) > 1024 * 50:  # 50KB 制限（学習用）
                    send_msg(conn, {'type': 'error', 'message': 'file too large'})
                    continue
                with _storage_lock:
                    _storage[filename] = data
                send_msg(conn, {'type': 'resp', 'result': 'uploaded'})
            elif cmd == 'download':
                filename = req.get('filename')
                if not filename:
                    send_msg(conn, {'type': 'error', 'message': 'filename required'})
                    continue
                with _storage_lock:
                    data = _storage.get(filename)
                if data is None:
                    send_msg(conn, {'type': 'error', 'message': 'not found'})
                    continue
                send_msg(conn, {'type': 'resp', 'result': base64.b64encode(data).decode()})
            else:
                send_msg(conn, {'type': 'error', 'message': 'unknown cmd'})
    except Exception:
        # 学習用なので詳細は出力しない
        pass
    finally:
        conn.close()


def serve(host: str = HOST, port: int = PORT):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen()
        print(f'Auth server listening on {host}:{port}')
        while True:
            conn, addr = s.accept()
            t = threading.Thread(target=handle_authenticated, args=(conn, addr), daemon=True)
            t.start()


if __name__ == '__main__':
    serve()
