# # -*- coding:utf-8 -*-
# import requests
# import re
# import json
#
# # 导入 requests  re正则 json
#
# '''
# login
# 登录花瓣 获取session
# '''
#
#
# def login():
#     login_url = 'http://huaban.com/auth/'
#     # 登录地址
#     headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0",
#         "Accept": "application / json",
#         "Content-type": "application/x-www-form-urlencoded; charset=utf-8",
#         "Referer": "http://huaban.com/",
#     }
#     # 请求头信息
#
#     session = requests.session()
#     # sesson 会话
#
#     login_data = {
#         "email": "zengmumu%40126.com",
#         "password": "zmm123",
#         "_ref": "frame"
#     }
#
#     response = session.post(login_url, data=login_data, headers=headers, verify=False)
#     # 登录页面
#     getPic(session, 5)
#     # 获取图片，前5页
#
#
# '''
# getPic
# 解析页面中的图片地址
# session 会话信息
# num     最大是页数
# '''
#
#
# def getPic(session, num):
#     for i in range(1, num + 1):
#         response = session.get("http://huaban.com/search/?q=%E5%A5%B3%E7%A5%9E&category=photography&page=" + str(i))
#         # 获取页面信息("美女"文字编码后的结果是"%E5%A5%B3%E7%A5%9E" )
#         data = re.search('app\.page\[\"pins\"\] =(.*);\napp.page\[\"page\"\]', response.text, re.M | re.I | re.S)
#         # 提取到当前页面所在的所有图片信息
#         data = json.loads(data.group(1))
#         # 转换字符串为列表
#         for item in data:
#             url = "http://hbimg.huabanimg.com/" + item["file"]["key"]
#             # 拼接图片地址
#             index = item["file"]["type"].rfind("/")
#             type = "." + item["file"]["type"][index + 1:]
#             # 获取图片的类型
#             file_name = item["raw_text"]
#             # 获取图片的中文名
#             download_img(url, file_name, type)
#             # 下载图片
#
#
# '''
# 下载图片
# url        图片的地址
# name   图片的中文名
# type     图片的类型
# '''
#
#
# def download_img(url, name, type):
#     response = requests.get(url, verify=False)
#     # 使用requests 下载图片
#     index = url.rfind('/')
#     file_name = name + url[index + 1:] + type
#     # 获取图片的hash值
#     print("下载图片：" + file_name)
#     # 打印图片名称
#     save_name = "./photo/" + file_name
#     # 图片保存的地址(注意photo要自己建一个，与当前.py文件同一个文件夹)
#     with open(save_name, "wb") as f:
#         f.write(response.content)
#         # 写入图片到本地
#
#
# '''
# 定义主函数
# '''
#
#
# def main():
#     login()
#
#
# # 如果到模块的名字是__main__ 执行main主函数
# if __name__ == '__main__':
#     main()
#
