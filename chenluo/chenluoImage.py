# -*- coding:utf-8 -*-

import urllib2
import os
import re

#获取页面
def get_page():
    url = 'http://www.50s.cc/whole/1.html'
    req = urllib2.Request(url)
    res = urllib2.urlopen(req)
    page = res.read().decode('utf-8')
    return page

#获取图片链接，返回一个字典{‘电影名字’；‘url’}
def get_url():
    page = get_page()
    #正则匹配电影名字和图片链接
    pat = re.compile('<div class="movie-item-in".*?<a.*?<img.*?src="(.*?)"'
                     '.*?<div.*?<div.*?<h1.*?<a.*?>(.*?)</a>', re.S)
    items = re.findall(pat, page)
    urls={}
    for i in items:
        urls[i[1]]=i[0]

    return urls

#下载图片到image文件夹下
def get_image():
    urls=get_url()
    #image目录是否存在
    if not os.path.exists('image'):
        os.mkdir('image')
    #切换到image目录
    os.chdir('image')
    for key in urls:
        try:
            data=urllib2.urlopen(urls[key]).read()
            filename=key + '.jpg'
            print 'save' + filename
            f=open(filename,'wb')
            f.write(data)
            f.close()
        except:
            pass
    print 'success'

get_image()

