import re  # 正则表达式模块 专门用于字符串 匹配, 替换, 分割

import requests  # 模拟发送请求  # pip install requests


def change_title(title):
    new_title = re.sub('[\\\/\:\*\?\"\<\>\|]', '_', title)
    return new_title

for page in range(6, 11):

    try:
        #打印的时候显示爬多少页
        print(f'=======================正在抓取第{page}页数据=========================')
        # 1. 找数据对应的url连接地址
        if page == 1:
            url = 'https://v.6.cn/minivideo/getMiniVideoList.php?act=recommend&page=1&pagesize=30'
        else:
            url = f'https://v.6.cn/minivideo/getMiniVideoList.php?act=recommend&page={page}&pagesize=25'

        # user-agent 浏览器的身份标识
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'}

        # 2. 发送地址请求(包含了各种各样的数据)  ua 伪装    遇到请求不到数据的时候可以考虑伪装
        response = requests.get(url=url, headers=headers)
        # json数据: 数据返回的一种形式
        json_data = response.json()
        # pprint.pprint(json_data)

        # 3. 数据解析  字典: 数据容器
        data_list = json_data['content']['list']
        # print(data_list)


        # 数据类型  流程控制  数据容器 ...
        for data in data_list:
            title = data['title']  # 视频的标题  # mp4 avi rmvb flv awn...
            playurl = data['playurl']  # 视频地址
            # print(title, playurl)

            # 请求视频数据  视频数据  图片  音频  都属于二进制数据
            video_data = requests.get(url=playurl, headers=headers).content

            new_title = change_title(title)

            # 4. 数据的保存
            with open('video\\' + new_title + '.mp4', mode='wb') as f:
                f.write(video_data)
                print('保存完成:', new_title)
    except:
        continue
