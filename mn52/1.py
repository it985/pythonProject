import requests
import re
from bs4 import BeautifulSoup
import time
import os

url = 'https://www.mn52.com/meihuoxiezhen/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
}

resp = requests.get(url, headers=headers)

# 把源码交给bs
main_page = BeautifulSoup(resp.text, 'html.parser')
h4List = main_page.find_all("h4")
h4List = h4List[:-2]  # 移除最后两个元素

p = re.compile(r'"(?P<href>.*?)"')
for item in h4List:
    child_href = 'https://www.mn52.com' + ''.join(p.findall(str(item)))  # 将bs4.element.Tag对象转为string对象
    # 拿到子页面的源代码
    child_page_resp = requests.get(child_href, headers=headers)
    # 文件夹命名
    p_name = re.compile(r'<div class="w740">.*?<h1>(?P<img_name>.*?)</h1>', re.S)
    img_name = p_name.findall(child_page_resp.text)
    img_name_f = ''.join(img_name)
    dirs = './img/' + img_name_f
    # 如果不存在这个文件夹就创建这个文件夹
    if not os.path.exists(dirs):
        os.makedirs(dirs)

    # 把源代码交给bs
    child_page = BeautifulSoup(child_page_resp.text, 'html.parser')
    imgList = child_page.find('div', id='piclist').find_all('img')

    num = 1
    for item in imgList:
        src = 'https://www.mn52.com' + item.get('src')
        # 下载图片
        img_resp = requests.get(src)
        # img_resp.content # 这里拿到的是字节
        with open(f'{dirs}/{num}.jpg', 'wb') as f:
            f.write(img_resp.content)
            num += 1
    print('over!!!')
    time.sleep(1)  # 缓一秒爬取

print('Game Over!!!')
resp.close()
