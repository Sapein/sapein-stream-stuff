#! /usr/bin/python3
import http.server
import json
import ssl
import struct
import urllib.request

import listen
import config

def release_key(app_key):
    url = 'https://id.twitch.tv/oauth2/revoke?client_id={}&token={}'.format(config.twitch_client_id, app_key)
    req = urllib.request.Request(url, method="POST")
    try:
        with urllib.request.urlopen(req, context=ssl.SSLContext()) as page:
            pass
    except urllib.error.HTTPError as e:
        print(e.code())
        print(e.read())
        raise

def get_twitch_id():
    url=("https://id.twitch.tv/oauth2/token"
         "?client_id={}"
         "&client_secret={}"
         "&grant_type=client_credentials").format(config.twitch_client_id, config.twitch_client_secret)
    req = urllib.request.Request(url, method='POST')
    try:
        with urllib.request.urlopen(req, context=ssl.SSLContext()) as page:
            data = json.loads(page.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        print(e.code)
        print(e.read())
        raise

    app_key = data['access_token']
    header = {'Authorization':'Bearer {token}'.format(token=app_key)}
    url="https://api.twitch.tv/helix/users?login={login_name}".format(login_name=config.twitch_username)
    req = urllib.request.Request(url, headers=header)
    try:
        with urllib.request.urlopen(req, context=ssl.SSLContext()) as page:
            data = json.loads(page.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        print(e.code)
        print(e.read())
        raise
    uid = data['data'][0]['id']
    config.app_key = app_key
    return uid

def subscribe():
    if not config.twitch_user_id:
        config.twitch_user_id = get_twitch_id()
        print("Your Client ID: {}".format(config.twitch_user_id))
    header={'Client-ID':config.twitch_client_id, 'Content-Type':'application/json'}
    u_data = ('{{"hub.mode":"subscribe",'
              '"hub.topic":"https://api.twitch.tv/helix/users/follows?first=1&to_id={}",'
              '"hub.callback":"{}",'
              '"hub.secret":"{}"}}').format(config.twitch_user_id, config.url, config.secret)
    dataa=u_data.encode('utf-8')
    header['Content-Length'] = len(dataa)
    header['User-Agent'] = 'twitchtest'
    req = urllib.request.Request('https://api.twitch.tv/helix/webhooks/hub', data=dataa, headers=header, method='POST')
    ret_data = urllib.request.urlopen(req, context=ssl.SSLContext())
    ret_code = ret_data.getcode()
    if ret_code == 200:
        print("Denied!")
        import sys;sys.exit(1)
    elif ret_code == 202:
        print("Accepted!")
        server_class = http.server.HTTPServer
        httpd = server_class(("", 8080), listen.HookHandler)
        httpd.handle_request()

def unsubscribe():
    header={'Client-ID':config.twitch_client_id, 'Content-Type':'application/json'}
    u_data = ('{{"hub.mode":"unsubscribe",'
              '"hub.topic":"https://api.twitch.tv/helix/users/follows?first=1&to_id={}",'
              '"hub.callback":"{}"}}').format(config.twitch_user_id, config.url)
    dataa=u_data.encode('utf-8')
    header['Content-Length'] = len(dataa)
    header['User-Agent'] = 'twitchtest'
    req = urllib.request.Request('https://api.twitch.tv/helix/webhooks/hub', data=dataa, headers=header, method='POST')
    ret_data = urllib.request.urlopen(req, context=ssl.SSLContext())
    ret_code = ret_data.getcode()
    if ret_code == 200:
        print("Denied!")
        import sys;sys.exit(1)
    elif ret_code == 202:
        print("Accepted!")
        server_class = http.server.HTTPServer
        httpd = server_class(("", 8080), listen.HookHandler)
        httpd.handle_request()

def main():
    with open("{}websub".format(config.FIFO_locations), 'w') as f:
        f.write("")
    httpd = http.server.HTTPServer(("", 8080), listen.HookHandler))
    httpd.serve_forever()

if __name__ == "__main__":
    try:
        subscribe()
        main()
    except KeyboardInterrupt:
        pass
    finally:
        unsubscribe()
        release_key(config.app_key)
