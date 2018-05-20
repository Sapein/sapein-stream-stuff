import urllib.request
import listen
import config
import ssl


def subscribe():
    header={'Client-ID':config.twitch_client_id, 'Content-Type':'application/json'}
    u_data = ('{{"hub.mode":"subscribe",'
              '"hub.topic":"https://api.twitch.tv/helix/users/follows?first=1&to_id={}",'
              '"hub.callback":"{}"}}').format(config.twitch_user_id, config.url)
    dataa=u_data.encode('utf-8')
    header['Content-Length'] = len(dataa)
    header['User-Agent'] = 'twitchtest'
    req = urllib.request.Request('https://api.twitch.tv/helix/webhooks/hub', data=dataa, headers=header, method='POST') 
    print(req.data)
    print(req.headers)
    ret_data = urllib.request.urlopen(req, context=ssl.SSLContext())
    ret_code = ret_data.getcode()
    if ret_code == 200:
        print("Denied!")
        import sys;sys.exit(1)
    elif ret_code == 202:
        print("Accepted!")
        server_class = listen.TwitchServer
        httpd = server_class(("", 8080), listen.HookHandler, None)
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
    print(req.data)
    print(req.headers)
    ret_data = urllib.request.urlopen(req, context=ssl.SSLContext())
    ret_code = ret_data.getcode()
    if ret_code == 200:
        print("Denied!")
        import sys;sys.exit(1)
    elif ret_code == 202:
        print("Accepted!")
        server_class = listen.TwitchServer
        httpd = server_class(("", 8080), listen.HookHandler, None)
        httpd.handle_request()

def main():
    pass

if __name__ == "__main__":
    try:
        subscribe()
        main()
    except KeyboardInterrupt:
        pass
    finally:
        unsubscribe()
