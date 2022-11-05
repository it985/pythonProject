# -*- codeing = utf-8 -*-
# @Time : 2021/6/19 23:01
# @Author : xiaow
# @File : PhotoSpider.py
# @Software : PyCharm
from bs4 import BeautifulSoup  # 网页解析
import xlwt  # excel操作
import sqlite3  # 数据库操作
from api import spider2 as spider
import time
from api import FileDownload as fd
import re  # 正则表达式

imglink = re.compile(r'<a href="(.*?)" target="_blank" title=".*?"><img alt=".*?" src=".*?"/><b>.*?</b></a>', re.S)
img2link = re.compile(r'<a href="(.*?)" target="_blank">.*?<span>（1680x1050）</span></a>', re.S)
img3link = re.compile(r'<img alt=".*?" src="(.*?)" title=".*?"/>', re.S)

# 获取照片页面路径
def getPhoto(url):
    srcs = []
    html = spider.askURL(url);
    bs = BeautifulSoup(html, "html.parser");
    for item in bs.find_all('a', target="_blank"):
        item = str(item)
        src = re.findall(imglink, item)
        if (len(src) != 0):
            srcs.append("http://www.netbian.com" + src[0])
    return srcs;

# 照片主页显示的照片不够清楚，这里根据这个网站存储照片的规律，拼接了一个地址，这个地址的照片比较高清一些
def getPhotoUrl(url):
    purls = [];
    url3 = "http://www";
    url2 = url.split(".")
    for j in range(1, len(url2)):
        if j == len(url2) - 2:
            url3 = url3 + "." + url2[j] + "-1920x1080"
        else:
            url3 = url3 + "." + url2[j]
    return (url3)
# 下载照片
def downloadPhoto(url):
    html = spider.askURL(url);
    bs = BeautifulSoup(html, "html.parser");
    for item in bs.find_all("img"):
        item=str(item)
        itemsrc=re.findall(img3link,item)
        if(len(itemsrc)!=0):
           return itemsrc[0]


if __name__ == '__main__':
    src = "http://www.netbian.com/mei/index_";
    # 拼接照片主页的路径
    for i in range(2,163):
        time.sleep(5)
        src2 = "";
        src2=src+str(i)+".htm"
        urls=getPhoto(src2)

        for j in range(len(urls)):
            time.sleep(3)
            fd.downloadFile('//photo//hd'+str(time.time())+".jpg",downloadPhoto(getPhotoUrl(urls[j])))

