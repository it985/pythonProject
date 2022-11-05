import requests
import os
from lxml import etree

# 创建文件夹
try:
    os.mkdir('./4k图片爬取')
except Exception:
    print('文件已创建！')

for i in range(2, 172):

    i = str(i)

    # 目录页面
    ml_url = 'http://pic.netbian.com/4kmeinv/index_' + i + '.html'

    # UA伪装请求头
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chromeh/81.0.4044.138 Safari/537.36'
    }

    response = requests.get(url=ml_url, headers=header)

    # 通用处理中文乱码的解决方法
    res = response.text.encode('iso-8859-1')

    treee = etree.HTML(res)

    t = treee.xpath('//div[@class="slist"]/ul/li')

    for tu in t:
        http = 'http://pic.netbian.com'
        # 标题
        tit = tu.xpath('./a/img/@alt')[0]
        # 地址
        tp = http + tu.xpath('./a/img/@src')[0]

        img = requests.get(url=tp, headers=header).content

        imgpath = './4k图片爬取/' + tit + '.jpg'

        with open(imgpath, 'wb') as fp:
            # 传入二进制内容
            fp.write(img)

            print(tit, '下载成功！')