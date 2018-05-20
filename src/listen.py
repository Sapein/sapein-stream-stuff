import http.server
import urllib.parse
import sys
import time
import json

class TwitchServer(http.server.HTTPServer):
    def __init__(self, server_address, RequestHandlerClass, challenge, bind_and_activate=True):
        self.challenge=challenge
        super().__init__(server_address, RequestHandlerClass, bind_and_activate)

    def finish_request(self, request, client_address):
        self.RequestHandlerClass(request, client_address, self, self.challenge)

class HookHandler(http.server.BaseHTTPRequestHandler):
    server_version = "HookHandler/0.1"

    def __init__(self, request, client_address, server, challenge=None):
        self.challenge=challenge
        super().__init__(request, client_address, server)

    def do_GET(s):
        challenge_token = s.requestline.split('challenge=')[1].split('&')[0]
        s.send_response(200, challenge_token.encode('utf-8'))

    def do_POST(s):
        print(s.headers)
        length = int(s.headers['Content-Length'])
        post_data = s.rfile.read(length).decode("utf-8")
        print("data")
        print(post_data)
        print("data")
        s.send_response(200, self.challenge.encode('utf-8'))

if __name__ == "__main__":
    server_class = http.server.HTTPServer
    httpd = server_class(("", 8080), HookHandler)
    print(time.asctime())
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
