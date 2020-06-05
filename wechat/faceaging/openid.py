import requests
APPID="wx00e942ceb5bea90a"
APPSECRET="d66b5afe89e0a9db378f98f3a4e65c06"

class OpenId:
    def __init__(self, jscode):
        self.url = 'https://api.weixin.qq.com/sns/jscode2session'
        self.app_id = APPID #env.str('APPID')
        self.app_secret = APPSECRET #env.str('APPSECRET')
        self.jscode = jscode

    def get_openid(self):
        url = self.url + "?appid=" + self.app_id + "&secret=" + self.app_secret + "&js_code=" + self.jscode + "&grant_type=authorization_code"
        res = requests.get(url)
        try:
            openid = res.json()['openid']
            session_key = res.json()['session_key']
        except KeyError:
            return 'fail'
        else:
            return openid, session_key
