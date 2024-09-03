# import requests
# import urllib.parse
# import json
# import jsonpath
# import os
# #https://www.duitang.com/napi/blog/list/by_search/?kw=%E5%8F%AF%E7%88%B1&type=feed&include_fields=top_comments%2Cis_root%2Csource_link%2Citem%2Cbuyable%2Croot_id%2Cstatus%2Clike_count%2Clike_id%2Csender%2Calbum%2Creply_count%2Cfavorite_blog_id&_type=&start=48
#
# header = {
#         'User-Agent':'Mozilla/5.0(Macintosh;Inter Mac OS X 10_13_3) AppleWebkit/537.36 (KHTML,like Gecko)'
#                      'Chrom/65.0.3325.162 Safari/537.36'
#     }
# #                                                    换成{}格式化输出
# url = 'https://www.duitang.com/napi/blog/list/by_search/?kw={}&start={}'
# #kw字段可自行更改，想搜什么写什么！！！
# kw = '美女'
# #调用方法进行加密
# kws = urllib.parse.quote(kw)
# # print(kw)
# # exit()
# num = 1
# #遍历0-241，每遍历一次跨度24个单位
# for start in range(0,241,24):
# #url.format方法是往{}内填充
#     urls = url.format(kws,start)
#     response = requests.get(urls,headers = header).text
#     html = json.loads(response)
#     #从html中提取数据   $:根节点  ..:下面的所有  path属性
#     photos = jsonpath.jsonpath(html,'$..path')
#     #print(photos)
#
#     def mkdir(path):
#
#         folder = os.path.exists(path)
#
#         if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
#             os.mkdir(path)  # mkdir 创建文件时如果路径不存在会创建这个路径
#             print
#             "---  new folder...  ---"
#             print
#             "---  OK  ---"
#
#         else:
#             print
#             "---  There is this folder!  ---"
#     #文件夹存放路径，自行更改
#     path = 'E:/itheima149/code/com/pythonProject/duitang/duitang/%s'%kw
#     mkdir(path)
#
#
#     for i in photos:
#         try:
#             a = requests.get(i)
#             with open('{}/{}.jpg'.format(path,num),'wb')as f:
#                 print('正在下载第：%s张图片'%num)
#             #所有二进制图片都得这么存储
#                 f.write(a.content)
#                 num += 1
#         except:
#             pass
#     print("第一页获取完成")
