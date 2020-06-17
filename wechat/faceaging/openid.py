import requests
APPID=""
APPSECRET=""

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
