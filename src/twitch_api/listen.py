import config
import http.server
import urllib.parse
import urllib.request
import hashlib
import struct
import sys
import time
import json

class HookHandler(http.server.BaseHTTPRequestHandler):
    server_version = "HookHandler/0.1"

    def do_GET(s):
        challenge_token = s.requestline.split('challenge=')[1].split('&')[0]
        s.send_response(200, challenge_token.encode('utf-8'))

    def do_POST(s):
        signature = s.headers['X-Hub-Signature']
        length = int(s.headers['Content-Length'])
        post_data = s.rfile.read(length).decode("utf-8")
        if signature = hashlib.sha256(post_data).hexdigest():
            print("data")
            decoded_data = json.load(post_data)
            header = {'Authorization':'Bearer {token}'.format(token=config.app_key)}
            url="https://api.twitch.tv/helix/users?login={login_name}".format(login_name=config.twitch_username)
            req = urllib.request.Request(url, headers=header)
            try:
                with urllib.request.urlopen(req, context=ssl.SSLContext()) as page:
                    data = json.loads(page.read().decode('utf-8'))
            except urllib.error.HTTPError as e:
                print(e.code)
                print(e.read())
                raise
            uid = data['data'][0]['display_name']
            try:
                req_id = data['id']
            except KeyError:
                try:
                    req_id = data['data']['id']
                except KeyError:
                    req_id = 0
            send_struct = struct.pack('LiLs', req_id, 0, len(uid), uid)
            with open("{}twitch_websub".format(config.FIFO_locations), 'w') as f:
                f.write(send_struct)
            print("data")
            s.send_response(200)
        else:
            print("Data does not hash properly!")
            s.send_response(200)


if __name__ == "__main__":
    server_class = http.server.HTTPServer
    httpd = server_class(("", 8080), HookHandler)
    print(time.asctime())
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
