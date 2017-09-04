# -*- coding:utf-8 -*-

import threading
import urllib2
import csv
import Queue
from lxml import etree
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

crawl_Exit = False
parser_Exit = False


class crawl_Tread(threading.Thread):
    def __init__(self, treadName, url_Queue, page_Queue):
        threading.Thread.__init__(self)  # 实例化是调用__inint__()
        self.treadName = treadName
        self.url_queue = url_Queue
        self.page_Queue = page_Queue

    def run(self):
        print '爬取线程' + self.treadName + '启动\n'
        self.crawl_Spider()

    def crawl_Spider(self):
        while True:
            if crawl_Exit:
                break
            else:
                print '开始加载网页:'
                url = self.url_queue.get()
                print url
                try:
                    req = urllib2.Request(url)
                    page = urllib2.urlopen(req).read()
                    self.page_Queue.put(page)
                except:
                    print url + ':爬取失败，即将爬取下一个页面\n'
                    pass
        print '网页加载完毕，马上开始解析\n'


class parser_Thread(threading.Thread):
    def __init__(self, threadName, page_Queue, queueLock):
        threading.Thread.__init__(self)
        self.threadName = threadName
        self.page_Queue = page_Queue
        self.queueLock = queueLock

    def run(self):
        print '解析线程' + self.threadName + '启动'
        self.parser()

    def parser(self):
        while True:
            if parser_Exit:
                break
            else:
                page = self.page_Queue.get()
                try:
                    text = etree.HTML(page)
                    node_list = text.xpath('//dl[@class="j-every clearfix"]')

                    self.queueLock.acquire()  # 加锁

                    with open('ganji.csv', 'ab') as filename:
                        writer = csv.writer(filename)
                        for node in node_list:
                            position = node.xpath('dt/a')[0].xpath('string()')
                            tag = node.xpath('dt/em/text()')[0].strip('(').strip(')')
                            if len(node.xpath('dd/a/text()')):
                                address = node.xpath('dd/a/text()')[0]
                            else:
                                address = ''

                            writer.writerow([position, tag, address])
                    filename.close()

                    queueLock.release()  # 释放锁
                    print '解析完成\n'
                except:
                    print '页面解析失败。。。。。。即将解析下一个页面。。。。。。。\n'
                    pass


crawl_list = ['crawl-1', 'crawl-2', 'crawl-3']
parser_list = ['parser-1', 'parser-2', 'parser-3']

url_Queue = Queue.Queue(10)
page_Queue = Queue.Queue(10)
queueLock = threading.Lock()

if __name__ == "__main__":
    position_name = raw_input('请输入您要搜索的职位名称：')
    page_num = raw_input('请输入需要爬取的页数：')

    while True:
        if page_num.isdigit():
            i = int(page_num)
            break
        else:
            print '请输入数字'

    base_url = 'http://cd.ganji.com/site/s/_%s' % (position_name)
    url_Queue.put(base_url)

    offset = 32

    while offset <= i * 32:
        url = 'http://cd.ganji.com/site/s/f' + str(offset) + '/_' + position_name
        print url
        url_Queue.put(url)
        offset += 32

    # 启动爬取线程

    threads = []

    for crawl in crawl_list:
        thread = crawl_Tread(crawl, url_Queue=url_Queue, page_Queue=page_Queue)
        thread.start()
        threads.append(thread)

    for parser in parser_list:
        thread = parser_Thread(parser, page_Queue=page_Queue, queueLock=queueLock)
        thread.start()
        threads.append(thread)

    while not url_Queue.empty():
        pass
    crawl_Exit = True

    while not page_Queue.empty():
        pass
    parser_Exit = True

    for t in threads:
        t.join()

    print '程序退出'
