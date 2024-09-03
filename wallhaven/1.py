import requests
from bs4 import BeautifulSoup
import os

# 循环爬取壁纸网站图片

def catchImg(url, page):

    # 请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36'
    }

    res = requests.get(url=url + '?page=' + page, headers=headers)
    # 解析数据
    soup = BeautifulSoup(res.text, 'html.parser')
    items = soup.find_all(class_='preview')

    for item in items:
        link = item['href']
        resUel = requests.get(url=link, headers=headers).text
        soup1 = BeautifulSoup(resUel, 'html.parser').find('img', id='wallpaper')['src']
        soup1_content = requests.get(url=soup1, headers=headers).content
        directory = 'img'
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(directory + '\\' + soup1[-20:-4] + '.jpg', mode='ab') as f:
            f.write(soup1_content)
            print(soup1)

for i in range(10):
    page = 2
    link = 'https://wallhaven.cc/toplist'
    # link = 'https://wallhaven.cc/hot'
    catchImg(link, str(page))
    page += 1
