# -*- coding:utf-8 -*-

import csv
import time
import urllib2
from lxml import etree
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/55.0',
    'Referer': 'https://www.lagou.com/zhaopin/Java/?labelWords=label'
}


def get_homePage():
    url = 'https://www.lagou.com/'

    req = urllib2.Request(url, headers=headers)
    page = urllib2.urlopen(req).read()

    return page


def get_menuUrl(page):
    data = etree.HTML(page)

    urls = []
    node_list = data.xpath('.//*[@id="sidebar"]/div/div[1]/div[@class="menu_sub dn"]/dl')

    for node in node_list:
        url_list = node.xpath('dd/a/@href')
        for url in url_list:
            urls.append(url)

    print '获取到职位列表，总计:%s条' % (str(len(urls)))
    return urls


def parser_positionList_page(urls):
    for url in urls:
        print '开始解析：%s' % url
        time.sleep(5)
        try:
            req = urllib2.Request(url, headers=headers)
            text = urllib2.urlopen(req).read()

            data = etree.HTML(text)

            node_list = data.xpath('.//ul[@class="item_con_list"]/li')

            print '正在解析%s条数据' % (str(len(node_list)))

            nextPage_url = data.xpath('//div[@class="item_con_pager"]/div/a[6]/@href')[0]
            print 'nextpage' + nextPage_url

            print '正在保存数据。。。。。'
            parser_save_Position(node_list)
            print '保存数据完成。。。休眠七秒'
            time.sleep(7)

            while True:
                print nextPage_url
                try:
                    print '开始解析子页面。。。。。。'
                    req = urllib2.Request(nextPage_url, headers=headers)
                    text = urllib2.urlopen(req).read()

                    data = etree.HTML(text)

                    node_list = data.xpath('.//ul[@class="item_con_list"]/li')

                    print '子页面加载成功，共%s条数据' % (len(node_list))
                    has_nextPage_url = data.xpath('//div[@class="item_con_pager"]/div/a[last()]/@href')
                    if has_nextPage_url[0] == "javascript:;":
                        nextPage_url = ''
                        break
                    else :

                        print '开始保存职位信息。。。。。'
                        parser_save_Position(node_list)
                        print '保存信息完成。。。。。\n'
                        nextPage_url=has_nextPage_url[0]
                        print '下一个页面是' + nextPage_url

                        print '休眠十秒----1'
                        time.sleep(10)

                except:
                    print '发生错误----1'
                    print '休眠三秒----1'
                    time.sleep(3)
                    pass

            print '休眠十二秒------2'
            time.sleep(12)
        except:
            print '发生错误------2'
            print '休眠三秒----2'
            time.sleep(3)
            pass


def parser_save_Position(node_list):
    for node in node_list:
        position = node.xpath('div[1]/div[1]/div[1]/a/h3/text()')[0]
        salary = node.xpath('div[1]/div[1]/div[2]/div[1]/span/text()')[0]
        address = node.xpath('div[1]/div[1]/div[1]/a/span/em/text()')[0]
        company = node.xpath('div[1]/div[2]/div[1]/a/text()')[0]

        f = open('lagou.csv', 'a')
        excel = csv.writer(f)
        excel.writerow([position, salary, address, company])
        f.close()


if __name__ == "__main__":
    page = get_homePage()
    urls = get_menuUrl(page)
    parser_positionList_page(urls)
