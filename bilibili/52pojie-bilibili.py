import requests
import os
from bs4 import BeautifulSoup

def download_images(url):
    # 发送HTTP请求获取网页源代码
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    html = response.text

    # 使用BeautifulSoup解析HTML内容
    soup = BeautifulSoup(html, 'html.parser')

    # 创建一个目录用于保存图片
    os.makedirs('bilibili_images', exist_ok=True)

    # 找到所有图片的标签
    img_tags = soup.find_all('img')

    # 遍历所有图片标签，下载图片
    for img in img_tags:
        img_url = img.get('data-src') or img.get('src')
        if img_url.startswith('//'):
            img_url = 'https:' + img_url

        # 下载图片
        response = requests.get(img_url)
        # 提取图片文件名
        img_file = img_url.split('/')[-1]
        # 将图片保存到指定目录下
        with open('bilibili_images/' + img_file, 'wb') as f:
            f.write(response.content)
            print(f"Downloaded: {img_file}")

# 要爬取的文章URL
article_url = 'https://www.bilibili.com/read/cv18302467/'
download_images(article_url)
