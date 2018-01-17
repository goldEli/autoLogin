# encoding utf-8
# https://10.0.8.46:18443/sefon-cas/login?service=https%3A%2F%2F10.0.8.49%3A18443%2Fminer%2F&locale=zh_CN

import requests
try:
    import cookielib
except:
    import http.cookiejar as cookielib
import re
import time
import os.path
try:
    from PIL import Image
except:
    pass

# 构造 Request headers
agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
headers = {
    "Host": "10.0.8.46:18443",
    "Referer": 'https://10.0.8.46:18443/sefon-cas/login?service=https%3A%2F%2F10.0.8.49%3A18443%2Fminer%2F%3Bjsessionid%3D4D863BE3C392D9B4D9D41F0444374937%3Bjsessionid%3D715BF58C5BEDAC561F586BDCE9F48295',
    "Accept-Language":"zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    'User-Agent': agent
}

url = 'https://10.0.8.49:18443/miner'

password  = '319a5d2ce2e52aaec8c09008ee85517f'
_eventId  = 'submit'
username  = 'admin'

def get_s_param():

    r = requests.post(url,verify=False,headers=headers)
    html = r.text
    execution = r'name="execution" value="(.*?)"'
    lt = r'name="lt" value="(.*?)"'

    a = re.findall(execution, html)
    b = re.findall(lt, html)

    return [a[0],b[0]]


# 获取验证码
def get_captcha():
    captcha_url = 'https://10.0.8.46:18443/sefon-cas/captcha'
    r = requests.post(captcha_url, headers=headers,verify=False)
    with open('captcha.jpg', 'wb') as f:
        f.write(r.content)
        f.close()
    # 用pillow 的 Image 显示验证码
    # 如果没有安装 pillow 到源代码所在的目录去找到验证码然后手动输入
    try:
        im = Image.open('captcha.jpg')
        im.show()
        im.close()
    except:
        print(u'请到 %s 目录找到captcha.jpg 手动输入' % os.path.abspath('captcha.jpg'))
    captcha = input("please input the captcha\n>")
    return captcha


def login():
    captcha = get_captcha()
    s_param = get_s_param()
    execution = s_param[0]
    lt        = s_param[1]

    postdata = {
        password: '319a5d2ce2e52aaec8c09008ee85517f',
        _eventId: 'submit',
        username: 'admin',
        execution: execution,
        lt: lt,
        captcha: captcha,
    }

    r = requests.post(url, data=postdata,headers=headers,verify=False)
    print(r.cookies)
    print(str(r))

login()

