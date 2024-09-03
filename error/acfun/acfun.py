import time

import requests  # 数据请求模块
import re  # 正则表达式模块
import json
import pprint

for page in range(3, 29):
    print(f'正在采集第{page}页的数据')
    time.sleep(1)
    link = 'https://www.acfun.cn/u/29946310'
    data = {
        'quickViewId': 'ac-space-video-list',
        'reqID': page+1,
        'ajaxpipe': '1',
        'type': 'video',
        'order': 'newest',
        'page': page,
        'pageSize': '20',
        't': '1653659024877',
    }
    headers = {
        'referer': 'https://www.acfun.cn/u/29946310',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36'
    }
    response = requests.get(url=link, params=data, headers=headers)
    # pprint.pprint(response.text)
    ac_id_list = re.findall('atomid.*?:.*?"(\d+).*?"', response.text)
    print(ac_id_list)


    for ac_id in ac_id_list:
        url = f'https://www.acfun.cn/v/ac{ac_id}'
        headers = {
            'referer': f'https://www.acfun.cn/u/{ac_id}',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36'
        }
        response = requests.get(url=url, headers=headers)
        title = re.findall('<title >(.*?) - AcFun弹幕视频网 - 认真你就输啦 \(\?ω\?\)ノ- \( ゜- ゜\)つロ</title>', response.text)[0]
        html_data = re.findall('window.pageInfo = window.videoInfo = (.*?);', response.text)[0]
        json_data = json.loads(html_data)
        m3u8_url = json.loads(json_data['currentVideoInfo']['ksPlayJson'])['adaptationSet'][0]['representation'][0]['backupUrl'][0]
        m3u8_data = requests.get(url=m3u8_url, headers=headers).text
        m3u8_data = re.sub('#E.*', '', m3u8_data).split()
        print(title)
        print(m3u8_url)
        for ts in m3u8_data:
            ts_url = 'https://ali-safety-video.acfun.cn/mediacloud/acfun/acfun_video/' + ts
            ts_content = requests.get(url=ts_url, headers=headers).content
            with open('video\\' + title + '.mp4', mode='ab') as f:
                f.write(ts_content)
            print(ts_url)
