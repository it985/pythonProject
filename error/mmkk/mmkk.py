import time
import requests
from bs4 import BeautifulSoup
import os
import random

url_pattern = "https://www.mmkk.me/category/weimei/{}/"

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.62',
    'Connection': 'keep-alive'
}
# 爬取前5页
for i in range(1, 6):
    time.sleep(10)
    url = url_pattern.format(i)
    response = requests.get(url=url, headers=headers)
    # 解码
    response.encoding = 'utf-8'
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    # 相册链接
    results = soup.find_all('a',attrs={"class":"item-link"})

    # 循环所有相册链接
    for j in results:
        time.sleep(random.randint(8,13))
        url_imgs = j.attrs['href']
        # 相册名
        path_name = j.get_text().strip()
        # 创建图片保存路径
        if not os.path.exists(path_name):
            os.makedirs(path_name, exist_ok=True)
        response_imgs = requests.get(url=url_imgs, headers=headers)
        # 解码
        response_imgs.encoding = 'utf-8'
        response_imgs.raise_for_status()
        soup_imgs = BeautifulSoup(response_imgs.text, 'html.parser')
        # 图片链接
        results_imgs = soup_imgs.find_all('div',attrs={"data-fancybox":"gallery"})
        # 循环所有图片链接
        for k in range(len(results_imgs)):
            img = results_imgs[k].attrs['data-src']
            file_name = path_name + '_' + str(k+1) + '.png'
            file_name = os.path.join(path_name, file_name)
            if not os.path.exists(file_name):
                time.sleep(random.randint(3,8))
                r = requests.get(img, headers=headers)
                if r.status_code == 200:
                    with open(file_name, 'wb') as f:
                        f.write(r.content)
