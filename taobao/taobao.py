#!/usr/bin/python
# -*- coding:utf-8 -*-
import urllib2
import json
import os


def get_image_urls():
    url = 'https://mm.taobao.com/tstar/search/tstar_model.do?_input_charset=utf-8'
    req = urllib2.Request(url)
    res = urllib2.urlopen(req)
    text = res.read().decode('gbk')

    items = json.loads(text)

    urls = []
    for i in items['data']['searchDOList']:
        urls.append(i['avatarUrl'])
        urls.append(i['cardUrl'])
    return urls


def down_images():
    urls = get_image_urls()

    try:
        os.mkdir('images')
    except:
        pass

    os.chdir('images')

    i = 1
    for url in urls:
        try:
            image_url = 'https:' + url
            data = urllib2.urlopen(image_url).read()
            # print image_url
            print 'save image:' + str(i) + '.jpg'
            f = open('%s.jpg'%(i), 'wb')
            f.write(data)
            f.close()
            i += 1
        except:
            pass


down_images()
