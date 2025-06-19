# coding:utf-8
# import urllib2
import re
import time
import urllib

import lxml.etree


# 获取每一页的链接
def geturlpage(name):
    url = "https://tieba.baidu.com/f?"
    word = {"kw": name}  # 贴吧的名字
    word = urllib.urlencode(word)  # 编码成字符串
    url = url + word  # 拼接url
    page = 20  # 假设要爬取贴吧前20页内容
    urlpage = []  # 设置一个空列表用于存放前20页链接
    # https://tieba.baidu.com/f?kw=%E7%BE%8E%E5%A5%B3&pn=0
    # print url
    # 将生成的链接添加到urlpage列表中
    for i in range(0, page):
        urlpage.append(url + str(i * 50))
    return urlpage


# 获取每个页面中的帖子的链接
def getpageurl(url):
    # 模拟浏览器头部
    headers = {
        "User-Agent": "Mozilla/5.0(WindowsNT6.1;rv:2.0.1)Gecko/20100101Firefox/60.0.1"
    }
    # request = urllib2.Request(url, headers=headers)  # 发起请求
    request = urllib.Request(url, headers=headers)  # 发起请求
    request.add_header("Connection", "keep-alive")  # 一直活着
    # response = urllib2.urlopen(request)  # 打开请求
    response = urllib.urlopen(request)  # 打开请求
    data = response.read()  # 读取数据
    # print data
    mystr = "<ul id=\"thread_list\" class=\"threadlist_bright j_threadlist_bright\">([\s\S]*?)<div class=\"thread_list_bottom clearfix\">"  # 抓取表格
    regex = re.compile(mystr, re.IGNORECASE)
    mylist = regex.findall(data)
    # print mylist
    table = mylist[0]
    mystr = "href=\"/p/(\d+)"  # 二次用正则表达式筛选选择恰当数据
    regex = re.compile(mystr, re.IGNORECASE)
    urltitlelist = regex.findall(table)
    # print mylist
    urllist = []
    for title in urltitlelist:
        urllist.append("http://tieba.baidu.com/p/" + title)
    return urllist


def downimg(url):
    # 模拟浏览器头部
    headers = {
        "User-Agent": "Mozilla/5.0(WindowsNT6.1;rv:2.0.1)Gecko/20100101Firefox/60.0.1"
    }
    # request = urllib2.Request(url, headers=headers)  # 发起请求
    request = urllib.Request(url, headers=headers)  # 发起请求
    request.add_header("Connection", "keep-alive")  # 一直活着
    # response = urllib2.urlopen(request)  # 打开请求
    response = urllib.urlopen(request)  # 打开请求
    data = response.read()  # 读取数据
    mytree = lxml.etree.HTML(data)
    jpglist = mytree.xpath("//*[@class=\"BDE_Image\"]/@src")  # 抓取图片（xpath）抓取方法
    return jpglist
    '''
     jpgnumbers = 10
    for jpgurl in jpglist:
        print "正在保存第"+str(jpgnumbers)+"图片......"
        urllib.urlretrieve(jpgurl, "jpg/" + str(jpgnumbers) + ".jpg")
        jpgnumbers += 1
    '''


# ++++++++++++++++++++++++++++++++++++++++++++++++++
jpgnumbers = 0

urlpagelsit = geturlpage("美女")
# urlpagelsit = geturlpage("%E7%BE%8E%E5%A5%B3")
for urlpage in urlpagelsit:
    print
    urlpage  # 打印每一页的链接
    time.sleep(1)
    urllist = getpageurl(urlpage)
    for iurllist in urllist:
        print
        iurllist
        time.sleep(1)
        jpglist = downimg(iurllist)
        for jpgurl in jpglist:
            print
            "正在保存第" + str(jpgnumbers) + "图片......"
            urllib.urlretrieve(jpgurl, "jpg/" + str(jpgnumbers) + ".jpg")
            jpgnumbers += 1 