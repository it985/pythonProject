# # 导入requests
# import requests  # 爬虫
# import json  # json解析
# import os  # 自动创建文件夹
# from urllib import request  # 下载图片
# import multiprocessing  # 多进程爬取多页
# import ssl
#
# # 模拟浏览器来访问
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
# }
#
#
# def get_huya_meizi(page=1):
#     '''
#     :param url: 下载路径
#     :return:
#     '''
#
#     # 开始爬取虎牙的妹子
#     response = requests.get(url, headers=headers)
#     content = response.text
#     result = content[len('getLiveListJsonpCallback('): -1]
#
#     # json解析: json字符串 => python字典
#     result2 = json.loads(result)
#
#     # 当前页的所有妹子
#     meizi_list = result2['data']['datas']
#     for meizi in meizi_list:
#         nick = meizi['nick']  # 昵称
#         img = meizi['screenshot']  # 图片url
#
#         # 下载图片,并以昵称作为图片名
#         try:
#             ssl._create_default_https_context = ssl._create_unverified_context
#             request.urlretrieve(img, f'huya/{nick}.png')
#             request.urlcleanup()  # 清空缓存
#             print(f'{nick}.png 下载完成!')
#         except Exception as e:
#
#             print('error:', e)
#
#
# if __name__ == '__main__':
#     # 自动创建huya文件夹
#     if not os.path.exists('huya'):
#         os.mkdir('huya')
#
#     # 获取虎牙妹子
#     # 使用多进程
#     for i in range(1, 3):
#         url = 'https://www.huya.com/cache.php?m=LiveList&do=getLiveListByPage&gameId=2168&tagAll=0&callback=getLiveListJsonpCallback&page=' + str(
#             i)
#         # 创建进程来同时获取多页数据
#         multiprocessing.Process(target=get_huya_meizi, args=(url,)).start()