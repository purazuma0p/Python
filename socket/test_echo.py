import threading
import time
import socket

# `test_echo.py` を直接パッケージ内から実行すると
# sys.path の最初の要素がパッケージのディレクトリになり
# `from socket_tutorial import server` が失敗します。
# そのためパッケージとしてのインポートを試み、失敗したら
# 同じディレクトリのモジュールを直接読み込みます。
try:
    from socket_tutorial import server
except Exception:
    import server


def _start_server_bg():
    # serve() は永続的に待ち受けするので別スレッドで起動
    t = threading.Thread(target=server.serve, daemon=True)
    t.start()
    return t


def test_echo():
    _start_server_bg()
    # サーバが立ち上がるまで少し待つ
    time.sleep(0.5)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('127.0.0.1', 65432))
        s.sendall(b'ping')
        data = s.recv(1024)

    assert data == b'ping'
    print('Test passed')


if __name__ == '__main__':
    test_echo()
