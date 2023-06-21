import requests
from bs4 import BeautifulSoup
import threading
import re
import time

album_urls = []  # 相册url列表
all_img_urls = []  # 所有图片

lock = threading.Lock()  # 互斥锁

headers = {
    "Host": "bcy.net",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:63.0) Gecko/20100101 Firefox/63.0"
}


# 抓取每个相册里面图片url
class ImgUrl(threading.Thread):

    def run(self):

        while len(album_urls) > 0:  # 只要不为空 就一直抓取
            lock.acquire()  # 上锁
            album_url = album_urls.pop()
            lock.release()  # 解锁

            try:
                response = requests.get(album_url, headers=headers, timeout=3)
                response.encoding = 'utf-8'
                re_obj = re.compile('"path(.*?)w650', re.S)
                r = (re_obj.findall(response.text))
                print("正在分析" + album_url)
                after_bs = BeautifulSoup(response.text, 'lxml')

                lock.acquire()  # 上锁
                for title in after_bs.find_all('title'):
                    global album_title
                    album_title = (str(title.get_text())).split('-')[0]

                for i in range(len(r)):
                    img_url = r[i].replace(r'\\u002F', '/')[5:] + 'w650.jpg'  # 拼接字符串，完成每张图片url

                    img_dict = {album_title: img_url}  # 相册名和图片url存入字典
                    all_img_urls.append(img_dict)
                print(album_title + '获取成功')

                lock.release()  # 解锁
                time.sleep(0.5)
            except:
                pass


# 获取相册url
class AlbumUrl():

    def __init__(self, url, url2):
        self.url = url
        self.url2 = url2

    def page(self, start, end):

        for i in range(start, end):

            url = self.url % i
            response = requests.get(url, headers=headers)

            response.encoding = 'utf-8'
            after_bs = BeautifulSoup(response.text, 'lxml')

            li_s = after_bs.find_all('li', class_='js-smallCards _box')  # 提取li标签内容

            for li in li_s:
                list_a = li.find_all('a', class_='db posr ovf')  # 提取a标签内容
                for a in list_a:
                    a_href = a.get('href')  # 取出部分url 进行拼接
                    album_urls.append(self.url2 + a_href)


if __name__ == '__main__':
    url = 'https://bcy.net/coser/index/ajaxloadtoppost?p=%s'
    url2 = 'https://bcy.net'
    spider = AlbumUrl(url, url2)
    spider.page(1, 5)  # 分析出来的页数
    for x in range(5):
        t = ImgUrl()
        t.start()