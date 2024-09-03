import requests


headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Mobile Safari/537.36"
}
down_path = "E:\itheima149\code\com\pythonProject\douying"
total_cursor = 7  # 一共75集，偏移了7页
per_count = 10  # 每页10集
short_url = "https://v.douyin.com/e4BxGEn/"  # 合集短连接地址
main_url = requests.get(url=short_url, headers=headers).url  # 获取合集地址栏url
mix_id = main_url.split("/")[6]  # 使用切片获取合集id
prefix_url = "https://www.iesdouyin.com/web/api/mix/item/list/?mix_id="  # 【Requests URL】-前面部分
suffix_url = "&count={}".format(per_count) + "&cursor={}"  # 【Requests URL】-后面部分

for cursor in range(total_cursor + 1):
    page_url = prefix_url + mix_id + suffix_url.format(cursor * 10)     # 页面url
    page_json = requests.get(page_url).json()
    page_count = len(page_json["aweme_list"])  # 每个url.json()包含的视频数量
    for count in range(page_count):
        video_url = page_json["aweme_list"][count]["video"]["play_addr"]["url_list"][0]
        str_ep = "第" + str(cursor * 10 + count + 1) + "集："
        video_list.append((str_ep, video_url))
        video_name = str_ep + page_json["aweme_list"][count]["share_info"]["share_title"].replace(" ", "")  # 第几集名字
        video = requests.get(url=video_url, headers=headers).content  # 第几集的视频文件
        with open(down_path + str(video_name) + ".mp4", "wb") as f:
            f.write(video)
            f.close()
        print("第" + str(episodes) + "集下载完成，名字:" + video_name)