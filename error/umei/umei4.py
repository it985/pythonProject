# -*- coding: utf-8 -*-
"""
Created on Sun Dec 30 15:38:25 2018

@author: 球球
"""

import requests
import os
from requests.packages import urllib3
from pyquery import PyQuery as pq


def get_url1(url):
    headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) '
                              'AppleWebKit/537.36 (KHTML, like Gecko)'
                              ' Chrome/58.0.3029.110 Safari/537.36'
                              }
    urllib3.disable_warnings()
    html = requests.get(url, headers=headers, verify=False).text
    doc = pq(html)
    a = doc('.TypeList .TypeBigPics')
    for item in a.items():
        b = item.attr('href')
    #    print(b,'\n','\n')
        html2 = requests.get(b,headers = headers,verify = False).text
        doc2 = pq(html2)
        c = doc2('.ImageBody img')
        for item2 in c.items():
          d = item2.attr('src')
          print(d)

          root = "D://pics22223//"   # 根目录
          path=root+d.split('/')[-1]
          # 根目录加上url中以反斜杠分割的最后一部分，即可以以图片原来的名字存储在本地
          try:
              if not os.path.exists(root):    # 判断当前根目录是否存在
                  os.mkdir(root)              # 创建根目录
              if not os.path.exists(path):    # 判断文件是否存在
                  r=requests.get(d)
                  with open(path,'wb')as f:
                      f.write(r.content)
                      f.close()
                      print("文件保存成功",'\n','\n')
              else:
                  print("文件已存在")
          except:
              print("爬取失败")


if __name__ == '__main__':
    z = 1
    url = 'http://www.umei.cc/p/gaoqing/cn/'
    for i in range(z, z+1):
        url1 = url+str(i)+'.htm'
        print(url1)
        get_url1(url1)

