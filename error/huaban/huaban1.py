# /usr/bin/env python
# coding:utf-8

import json
import urllib.request
import threading


# 导入需要的JSON ，urllib及threading
# 定义一个类
class myThread(threading.Thread):
    def __init__(self, imgurl, filename):
        threading.Thread.__init__(self)
        self.imgurl = imgurl
        self.filename = filename

    def run(self):
        print('downloading: ' + self.imgurl)
        downfile(self.imgurl, self.filename)


# 定义一个下载程序
def downfile(imgurl, filename):
    img_req = urllib.request.Request(imgurl)
    opener = urllib.request.build_opener()
    img_resp = opener.open(img_req)
    try:
        out = open(filename, 'wb')
        out.write(img_resp.read())
        out.flush()
        out.close()
    except:
        print('error')


if __name__ == "__main__":

    surl = 'http://huaban.com/pins/1821121555/?jlb0k0ki'
    # 需要爬取的花瓣网美女图片地址
    hb = urllib.request.Request(surl)
    # 按XHLHttprequest方式请求
    hb.add_header('X-Requested-With', 'XMLHttpRequest')
    # 模拟win10 chrome 浏览器
    hb.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0')
    html = urllib.request.urlopen(hb).read()
    obj = json.loads(html)
    # print (obj['pin']['board']['pins'])
    imgs = obj['pin']['board']['pins']
    # 花瓣网图片需要的网址头
    preurl = 'http://img.hb.aicdn.com/'
    for img in imgs:
        imgurl = preurl + img['file']['key']
        # print (imgurl)
        myThread(imgurl, img['file']['key'] + '.jpg').start()

