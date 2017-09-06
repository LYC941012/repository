# coding=utf-8
from selenium import webdriver
from lxml import etree
import os
import urllib2

# 设置PhantomJS路径
driver = webdriver.PhantomJS(r'D:\Program Files (x86)\PythonTool\phantomjs-'
                             r'2.1.1-windows\bin\phantomjs.exe')
driver.get("http://huaban.com")

# 模拟点击“加载更多”按钮,这里模拟点击了三次
for i in range(3):
    driver.find_element_by_link_text('加载更多').click()

print '开始解析网页。。。。。。。。。。。。。。。'
data = etree.HTML(driver.page_source)
node_list = data.xpath('//div[@class="recommend-container-row clearfix"] | '
                       '//div[@id="recommend_container"]/div[@class="recommend-'
                       'container-row clearfix"]')

img_urls = []  # 用于保存图片链接
for node in node_list:
    urls = node.xpath('div[@class="recommend-imgbox recommend-box"]/a/img/@src | '
                      'div[@class="recommend-hidebox pl-right"]/'
                      'div[@class="recommend-imgbox recommend-box"]'
                      '/a/img/@src')

    for url in urls:
        img_urls.append(url)

# 创建“花瓣”目录保存图片
if os.path.exists('huaban'):
    pass
else:
    os.mkdir('huaban')
os.chdir('huaban')

i = 1

for img_url in img_urls:
    print "正在保存第%s张图片。。。。。" % (str(i))
    image = urllib2.urlopen('http:' + img_url).read()
    with open('%s.jpg' % (str(i)), 'wb') as f:
        f.write(image)
        f.close()
    i += 1
