import re

import requests

headers = {
    'cookie': 'SUB=_2AkMWuiaof8NxqwJRmfEcxW7kZYV1zQHEieKg5tdzJRMxHRl-yT8XqmlbtRB6PToIR8vzOUazMyBaDx1yoAhoGvmhBh2R; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WFhP5UbeyRGEMWCEO66rKKN; SINAGLOBAL=4378435525987.705.1642506657635; UOR=,,www.baidu.com; YF-V-WEIBO-G0=35846f552801987f8c1e8f7cec0e2230; _s_tentry=www.baidu.com; Apache=3198609812447.024.1647671292904; ULV=1647671293014:4:2:2:3198609812447.024.1647671292904:1647496624245; XSRF-TOKEN=ZPnKMpYcxCvUsgDmUWvm7Jwi',
    'origin': 'https://www.weibo.com',
    'page-referer': '/tv/channel/4379160563414111/editor',
    'referer': 'https://www.weibo.com/tv/channel/4379160563414111/editor',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36',
    'x-xsrf-token': 'ZPnKMpYcxCvUsgDmUWvm7Jwi',
}
def get_json(next_cursor):
    url = 'https://www.weibo.com/tv/api/component?page=%2Ftv%2Fchannel%2F4379160563414111%2F4379160563414139'
    data = {
        'data': '{"Component_Channel_Subchannel":{"cid":"4379160563414139"}}'
    }
    if next_cursor != -1:
        data = {
            'data': '{"Component_Channel_Subchannel":{"next_cursor":' + str(next_cursor) +', "cid":"4379160563414139"}}'
        }
    response = requests.post(url, headers=headers, data=data)
    json_data = response.json()
    if json_data['data']['Component_Channel_Subchannel'] != None:
        next_cursor = json_data['data']['Component_Channel_Subchannel']['next_cursor']
        if next_cursor == None:
            return 0
    else:
        return 0
    data_list = json_data['data']['Component_Channel_Subchannel']['list']
    for data in data_list:
        title = data['title'] + str(data['media_id'])
        title = re.sub(r'[\/:*?"<>|]', '', title)
        oid = data['oid']
        # print(title, oid)
        info_url = 'https://www.weibo.com/tv/api/component?page=' + oid
        data_1 = {
            'data': '{"Component_Play_Playinfo":{"oid":"'+oid+'"}}'
        }
        response_1 = requests.post(info_url, headers=headers, data=data_1)
        json_data_1 = response_1.json()
        print(json_data_1)
        if json_data_1['data']['Component_Play_Playinfo'] != None:
            dict_urls = json_data_1['data']['Component_Play_Playinfo']['urls']
            # dict_urls.keys(): 获取所有的键名称
            # list(): 转成了列表  [0]   list(dict_urls.keys())[0]: '高清 1080P'
            # dict_urls[ist(dict_urls.keys())[0]]: 最高清画质的视频链接
            video_sub = dict_urls[list(dict_urls.keys())[0]]
            video_url = 'https:' + video_sub
            print(title,video_url)
            video_data = requests.get(url=video_url).content
            with open(f'video/{title}.mp4', mode='wb') as f:
                f.write(video_data)
    get_json(next_cursor)

get_json(-1)
