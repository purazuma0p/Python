import threading
import time
import base64

try:
    from socket_tutorial import auth_server, auth_client
except Exception:
    import auth_server
    import auth_client


def _start_server():
    t = threading.Thread(target=auth_server.serve, daemon=True)
    t.start()
    return t


def test_auth_flow():
    _start_server()
    time.sleep(0.3)
    c = auth_client.AuthClient()
    assert c.connect() is True

    r = c.cmd('ping')
    assert r.get('type') == 'resp' and r.get('result') == 'pong'

    r = c.cmd('time')
    assert r.get('type') == 'resp'

    r = c.cmd('echo', data='abc')
    assert r.get('type') == 'resp' and r.get('result') == 'abc'

    # upload
    payload = b'hello world'
    r = c.cmd('upload', filename='foo.txt', data=base64.b64encode(payload).decode())
    assert r.get('type') == 'resp' and r.get('result') == 'uploaded'

    r = c.cmd('download', filename='foo.txt')
    assert r.get('type') == 'resp' and base64.b64decode(r.get('result').encode()) == payload

    c.close()
    print('Auth test passed')


if __name__ == '__main__':
    test_auth_flow()
