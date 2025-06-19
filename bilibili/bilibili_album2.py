# -*- By:QianJue   -*-
# -*- Coding:utf-8 -*-
import json
import os
import re
import requests
import sys


def loads_jsonp(_jsonp):
    """
    解析jsonp数据格式为json
    :return:
    """
    try:
        return json.loads(re.match(".*?({.*}).*", _jsonp, re.S).group(1))
    except:
        raise ValueError('Invalid Input')


if __name__ == '__main__':
    uid = input('请输入UID：')
    headers = {
        'user-agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36 Edg/89.0.774.68',
    }
    ban = ['<', '>', '/', '\\', '?', '*', ':', '|', '\n']
    name_url = 'https://space.bilibili.com/{0}'.format(uid)
    n_res = requests.get(name_url, headers=headers)
    html = n_res.text
    name = re.findall(r'<meta name="keywords" content="(.*?)"/>', html)[0].split(',')[0]
    if not os.path.exists(name):
        os.mkdir(name)
    for i in range(0, 100):
        url = 'https://api.bilibili.com/x/dynamic/feed/draw/doc_list?uid={0}&page_num={1}&page_size=50&biz=all&jsonp=jsonp'.format(
            uid,
            i)
        res = requests.get(url, headers=headers)
        if res.text == '{"code":0,"message":"0","ttl":1,"data":{"items":null}}':
            print('下载完毕')
            sys.exit(0)
        js = loads_jsonp(res.text)
        rename = 0
        for j in js['data']['items']:
            dir_name_ = j['description']
            dir_name = ''
            for s in dir_name_:
                if s in ban:
                    s = ''
                dir_name += s
            print(dir_name)
            if not os.path.exists(name + '/' + dir_name):
                try:
                    os.mkdir(name + '/' + dir_name)
                except OSError as o:
                    print(o)
                    dir_name = 'rename' + str(rename)
                    rename += 1
                    os.mkdir(name + '/' + dir_name)
            for n in j['pictures']:
                img_url = n['img_src']
                file_name = img_url.split('/')[-1]
                if not os.path.exists(name + '/' + dir_name + '/' + file_name):
                    img_res = requests.get(img_url, headers=headers)
                    try:
                        with open(name + '/' + dir_name + '/' + file_name, 'wb') as f:
                            f.write(img_res.content)
                    except:
                        print(name + '/' + dir_name + '/' + file_name + '下载失败')