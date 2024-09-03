import requests
import json
import time

def get_all_bv_numbers(up_id):
    bv_numbers = []
    page = 1
    while True:
        url = f'https://api.bilibili.com/x/space/arc/search?mid={up_id}&pn={page}&ps=50&jsonp=jsonp'
        response = requests.get(url)
        data = response.json()
        if data['code'] != 0:
            print(f"请求失败，错误信息：{data['message']}")
            break
        video_list = data['data']['list']['vlist']
        if len(video_list) == 0:
            break
        for video in video_list:
            bv_numbers.append(video['bvid'])
        page += 1
        time.sleep(100)  # 添加延迟，避免频繁请求
    return bv_numbers

# 示例用法
up_id = '140226477'  # 替换为您要获取bv号的up主的id
bv_numbers = get_all_bv_numbers(up_id)
print(bv_numbers)
