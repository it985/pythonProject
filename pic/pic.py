# --*-- coding:utf-8 --*--
# @FileName : mhy.py
# @Author   : Administrator
# @DateTime : 2022/10/29 16:06
# @Desc     : 读取同级目录下的 url.txt 文件，将文件中的 url 地址对应的图片进行下载
import os
import time
import random

import requests

# 请求头
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
}

# 随机字符串
s = 'abcdefghijklmnopqrstuvwxyz'

# 创建文件夹
try:
    os.mkdir('images')
except:
    pass


def down_image(file_name, url):
    """
    下载图片主程序
    :param file_name: 需要保存图片的文件名
    :param url: 需要下载的图片URL地址
    :return: 保存成功返回 TRUE 失败返回 FALSE
    """
    try:
        print('正在下载：' + url)
        with open('./images/' + file_name, 'wb') as f:
            f.write(requests.get(url=url, headers=headers).content)
        return True
    except:
        return False


# 读取需要下载的图片地址，存为列表
with open('url.txt', 'r', encoding='utf-8') as f:
    url_list = f.read().split('\n')

print('任务开始：共' + str(len(url_list)) + '个下载图片任务')

# 成功 or 失败 计数
count_0 = 0
count_1 = 0

for url in url_list:
    try:
        # 判断 URL 链接类型，如无图片格式，将自行存为 png 格式图片
        if '.png' in url or '.jpg' in url or '.jpeg' in url or '.webp' in url:
            # 分割URL，获取图片原本文件名
            file_name = url.split('/')[-1]
            down_image(file_name, url)
        else:
            # 时间戳后六位+随机4个字符串拼接，组成图片文件名
            file_name = str(time.time())[-6:] + random.choice(s) + random.choice(s) + random.choice(s) + random.choice(
                s) + '.png'
            down_image(file_name, url)
        count_1 += 1
    except:
        count_0 += 1

print('任务结束！')
print('爬取成功：' + str(count_1) + '\n爬取失败：' + str(count_0))
