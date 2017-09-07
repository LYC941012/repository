# -*- coding:utf-8 -*-

import urllib2
import urllib
import cookielib
import json

# 登录验证url
login_action_url = 'https://login.zhipin.com/login/account.json'

headers = {
    'Connection':'keep-alive',
    'User - Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/'
                    '537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Referer': 'https://login.zhipin.com/'
}

#这个不重要
randomKey = 'Bt8lEnlYPN4p3k8igDL51c9xYBtehN4D'

while True:
    #创建cookie
    cookie = cookielib.CookieJar()
    handler = urllib2.HTTPCookieProcessor(cookie)
    opener = urllib2.build_opener(handler)
    #获取验证码并保存
    QR_image = opener.open('https://login.zhipin.com/'
                           'captcha/?randomKey=' + randomKey +
                           '&_r=1504767809869').read()

    f = open('QR_code.jpg', 'wb')
    f.write(QR_image)
    f.close()

    username = raw_input('请输入账号(手机号码)：')
    password = raw_input('请输入密码：')
    QR_code = raw_input('请输入验证码(见QR_code.jpg)：')
    data = {
        'regionCode': '+86',
        'account': username,
        'password': password,
        'captcha': QR_code,
        'randomKey': randomKey
    }

    req = urllib2.Request(login_action_url, headers=headers, data=urllib.urlencode(data))

    response = opener.open(req).read()
    res = json.loads(response)

    print res
    if res['rescode'] == 7:
        print '用户名或密码错误,登录失败'
        randomKey = res['randomKey']

    elif res['rescode'] == 3:
        print '验证码错误，登陆失败'
        randomKey = res['randomKey']
    elif res['rescode'] == 1:
        print '登录成功'
        break

    else:
        print '未知错误'
#打印cookie信息
for item in cookie:
    print item.name
    print item.value

