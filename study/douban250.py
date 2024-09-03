import requests
import lxml
from bs4 import BeautifulSoup
from lxml import etree

url = 'https://movie.douban.com/top250'

hread = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
        'Referer': 'https://movie.douban.com/'
}
movies_list = list()

for page in range(0,10):
    # 访问多页面去获取250条数据
    _page = int(page) * 25

    href = url + '?start=' + str(_page) + '&filter='

    response = requests.get(href, headers=hread)

    boj = BeautifulSoup(response.text, 'lxml')

    movies_title = boj.find_all('div', class_='hd')

    for i in movies_title:
        print(i.a.span.text.strip())
