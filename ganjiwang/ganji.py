# -*- coding:utf-8 -*-
import urllib2
from lxml import etree
import csv
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


def getFirstPage(position):
    url = 'http://cd.ganji.com/site/s/_%s' % (position)
    print url
    req = urllib2.Request(url)
    page = urllib2.urlopen(req).read()

    return page


def praseHtml(page, filename):

    selector = etree.HTML(page)

    nextUrl = selector.xpath('.//li[@class="next"]/a/@href')

    node_list = selector.xpath('//dl[@class="j-every clearfix"]')

    writer = csv.writer(filename)
    writer.writerows([('职位', '类型', '公司地址')])
    print '正在保存职位信息。。。。。'
    for node in node_list:
        position = node.xpath('dt/a')[0].xpath('string()')

        tag = node.xpath('dt/em/text()')[0]

        addr = node.xpath('dd/a/text()')
        if len(addr):
            address = addr[0]
        else:
            address = ''
        data = [position, tag, address]

        writer.writerow(data)

    if not len(nextUrl):
        return 'end'
    else:
        return baseUrl + nextUrl[0]


def searchPosition(position, file_name):
    filename = open(file_name, 'a')

    fristPage = getFirstPage(position)
    url = praseHtml(fristPage, filename)
    print '正在解析第一页'

    while url != 'end':
        try:
            print '正在解析:' + url
            req = urllib2.Request(url)
            page = urllib2.urlopen(req).read()
            # print page

            url = praseHtml(page, filename)
        except:
            pass

    print '职位信息爬去完毕！'
    filename.close()

baseUrl = 'http://cd.ganji.com'
searchPosition('会计', 'ganji.csv')
