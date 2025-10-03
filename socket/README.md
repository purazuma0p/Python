# socket_tutorial

このフォルダは Python のソケット通信入門用の小さなチュートリアルです。

内容:

使い方（PowerShell）:

```powershell
# サーバを起動する（別のターミナルウィンドウで）
python .\socket_tutorial\server.py

# 別のターミナルでクライアントを実行
python .\socket_tutorial\client.py "こんにちは"

# テストを実行して動作確認（テストはサーバを別スレッドで起動して検証します）
python .\socket_tutorial\test_echo.py
```

学習ステップの提案:
1. 上のエコーサーバ/クライアントを動かす
2. 送受信するデータサイズを増やす、バイナリデータを送る
3. 複数クライアントを同時に扱う方法（`threading`→`selectors`→`asyncio`）
4. プロトコル設計（メッセージ長のプレフィックス、改行区切り、JSONなど）
5. 暗号化（TLS）や認証を追加して安全にする

注意:

追加した教材:
- `auth_server.py` - JSON-over-TCP、チャレンジ/レスポンス HMAC 認証を持つ安全サンプルサーバ
- `auth_client.py` - サーバに認証してコマンドを送れるクライアント
- `test_auth.py` - 認証と基本コマンドの自動テスト

要点:
- 認証はチャレンジ/レスポンス（HMAC）で行われます。サーバは16バイトのランダムノンスを送り、クライアントは共有シークレットで HMAC-SHA256 を計算して返します。
- メッセージは length-prefix (4 byte, big-endian) + JSON ボディでフレーム化されています。
- ファイルのアップロードはサイズ制限（50KB）を設けています。
