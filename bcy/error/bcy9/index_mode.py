import os
import re

import requests


def Requests(url, head):
    while True:
        try:
            response = requests.get(url, headers=head)
        except:
            print('链接失败')
        else:
            if response.status_code == 200:
                return response
            else:
                print('连接错误')


def img_index(host_url):
    head = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3741.400 QQBrowser/10.5.3863.400'}
    response = Requests(host_url, head)
    num = 0  # 用于后面的计算图片数目
    for Format in ('.jpg', '.png', ''):
        if Format == '':
            url = re.findall('https:(.{90,100}?)' + Format + '~tplv-banciyuan-w650.image', response.text)
        else:
            url = re.findall('https:(.{140,155}?)' + Format + '~tplv-banciyuan-w650.image', response.text)
        # 正则表达式匹配目标图片地址
        for i in url:
            num += 1
            a = i.replace('u002F', '').replace('\\\\', '/')  # 使用replace（）对字符串进行替换
            # 由于获取的图片地址含有u002F等无用字块在这里进行处理（可能是我技术问题，我获取的源码有点诡异）
            url = 'https:' + a + Format + '~tplv-banciyuan-w650.image'
            try:  # 如果出错就跳过并抛出问题网址，但不处理，跳过此网站
                r = requests.get(url, headers=head)
            except:
                print('出错啦:' + url)
            else:
                print(url)
                number = len(os.listdir(os.getcwd() + '/cos')) + 1
                if number <= 9:
                    number = '00' + str(number)
                elif 10 <= number < 100:
                    number = '0' + str(number)
                else:
                    number = str(number)

                if Format == '':
                    download_Format = '.jpg'
                else:
                    download_Format = Format
                open('./cos/' + number + download_Format, 'wb').write(r.content)
                print('保存成功')


def main(url):
    img_index(url)  # 创造接口


if __name__ == '__main__':
    main()
