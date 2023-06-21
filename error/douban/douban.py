# #-*- codeing = utf-8 -*-
# #@Time : 2021/3/1 16:16
# #@Author : xiaow
# #@File : spider2.py
# #@Software : PyCharm
#
# import re  # 正则表达式
# import sys
# import urllib.request, urllib.error  # 指定url，获取网页数据
# from bs4 import BeautifulSoup  # 网页解析
# import xlwt  # excel操作
# import sqlite3  # 数据库操作
#
# baseurl = 'https://movie.douban.com/top250?start='
#
# imglink = re.compile(r'<a href=".*?" title=".*?">', re.S)
#
# titlelink = re.compile(r'<span class="title">(.*)</span>')
# findlink = re.compile(r'<a href="(.*?)">')  # 创建正则表达式 表示规则
#
#
# # 1.爬取网页
# def getData(url):
#     urllist = []
#     valuelist = []
#     # 2.解析数据
#     img = []
#     src = []
#     title = []
#     for i in range(0, 10):
#         url = baseurl + str(i * 25)
#         html = askURL(url)
#         bs = BeautifulSoup(html, "html.parser")
#         print(bs)
#         urllist.append(bs.a.attrs["href"])
#         valuelist.append(bs.a.string)
#         return urllist, valuelist
#         for item in bs.find_all('div', class_="item"):  # 查找div 并且该div应满足class=item
#             print(item)
#             item = str(item)
#             titlel = re.findall(titlelink, item)
#             title.append(titlel)
#             srcl = re.findall(findlink, item)  # 正则表达式进行筛选
#             for s in srcl:
#                 src.append(s)
#             imgl = re.findall(imglink, item)  # 正则表达式进行筛选
#             for i in imgl:
#                 img.append(i)
#     return title, img, src;
#
#
# # 得到一个url的网页内容1
# def askURL(url):
#     head = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36",
#         "Cookie": '_ga=GA1.2.1191993538.1623990557; _gid=GA1.2.176559558.1623990557; HstCfa3699098=1623990557028; HstCmu3699098=1623990557028; HstCnv3699098=1; HstCns3699098=1; newurl=0; __dtsu=10401623990557D693AE61F09F524965; pbnfgecookieinforecord=%2C64-32128%2C64-32129%2C; HstCla3699098=1623991353818; HstPn3699098=7; HstPt3699098=7'
#     }
#     req = urllib.request.Request(url=url, headers=head)
#     html = ""
#     try:
#         response = urllib.request.urlopen(req)
#         html = response.read()
#     except Exception as result:
#         print(result)
#     return html
#
#
# # 3.保存数据
# def savaData(savepath):
#     pass
#
