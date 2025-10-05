import socket
#socket()→bind(now)→listen()→accept()→recv()→send()→close()
# サーバーのIPアドレスとポート番号
#サーバーのIPアドレスはこのプログラムをどうさせるマシンのIPアドレスになる
HOST = ''  # 空文字列で全てのインターフェースで待ち受け
PORT = 8000

# 1. ソケット作成
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 2. バインド（IPとポートを割り当て）
sock.bind((HOST, PORT))

# 3. リッスン（接続待ち状態にする）
sock.listen(1)
print(f'ポート{PORT}で接続待ち...')

# 4. アクセプト（クライアントからの接続を受け入れる）
conn, addr = sock.accept()
print(f'接続：{addr}')

# 5. データ受信
data = conn.recv(1024)
print(f'受信データ: {data.decode()}')

# 6. データ送信（例として「Hello, client!」を返す）
conn.sendall(b'Hello, client!')

# 7. コネクションとソケットをクローズ
conn.close()
sock.close()