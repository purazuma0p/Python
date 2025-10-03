import socket
import threading

HOST = '127.0.0.1'
PORT = 65432


def handle_client(conn, addr):
    """接続ごとに呼ばれるハンドラ。受け取ったデータをそのまま返す（エコー）。"""
    with conn:
        print(f'Connected by {addr}')
        while True:
            data = conn.recv(1024)
            if not data:
                break
            # エコー応答
            conn.sendall(data)


def serve(host: str = HOST, port: int = PORT):
    """シンプルなブロッキング TCP サーバ。新しい接続はスレッドで処理する。"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen()
        print(f'Server listening on {host}:{port}')
        while True:
            conn, addr = s.accept()
            t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            t.start()


if __name__ == '__main__':
    serve()
