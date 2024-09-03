# import json
#
# json_data = '''
# [
#     {"id":"5fe0a1a1-f186-42bd-a185-6c32074b3fee","name":"超兽武装.jpg","url":"https://article.biliimg.com/bfs/article/33f9d71c92d1b32e55283c3b5697d575ba2aa6f1.jpg","width":3840,"height":2160,"date":1690349846407},
#     {"id":"7a59e62a-4e4a-4c47-a6aa-71bef0dcfaa0","name":"家有儿女.jpg","url":"https://article.biliimg.com/bfs/article/6e0ff377577b6b95e2c32791f4cafc60c7dad4fe.jpg","width":480,"height":480,"date":1690349845767},
#     {"id":"9be6ad24-1038-4732-af37-f66497ecfb74","name":"45761e06e5d08201183a53961f3018fa.jpg","url":"https://article.biliimg.com/bfs/article/c354cd2180b100189d553d71e37c38daf45f6127.jpg","width":2730,"height":1534,"date":1690349845821}
# ]
# '''
#
# data = json.loads(json_data)
#
# for item in data:
#     url = item['url']
#     print(url)
# import json
#
# # 从本地文件读取 JSON 数据
# with open('B站图床数据-2023-07-26.json', 'r',encoding='utf-8') as file:
#     json_data = file.read()
#
# data = json.loads(json_data)
#
# for item in data:
#     name = item['name']
#     url = item['url']
#     print(f"{name}: {url}")
import glob
import json

# 使用通配符匹配文件名
file_pattern = 'B站图床数据-*.json'
file_list = glob.glob(file_pattern)

# 遍历匹配到的文件
for file_name in file_list:
    with open(file_name, 'r', encoding='utf-8') as file:
        json_data = file.read()
    data = json.loads(json_data)
    for item in data:
        name = item['name']
        url = item['url']
        print(f"{name}: {url}")
