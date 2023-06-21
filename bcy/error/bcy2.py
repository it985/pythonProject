# https://www.cnblogs.com/happymeng/p/10177303.html
import requests
from fake_useragent import UserAgent

if __name__ == '__main__':
	###  mongodb 的一些基本操作
    DATABASE_IP = '127.0.0.1'
    DATABASE_PORT = 27017
    DATABASE_NAME = 'sun'
    start_url = "https://bcy.net/circle/timeline/loadtag?since={}&grid_type=timeline&tag_id=399&sort=recent"
    client = MongoClient(DATABASE_IP, DATABASE_PORT)

    db = client.sun
    db.authenticate("dba", "dba")
    collection  =  db.bcy  # 准备插入数据
	#####################################3333
    get_data(start_url,collection)

## 半次元COS图爬取-获取数据函数
def get_data(start_url,collection):
    since = 0
    while 1:
        try:
            with requests.Session() as s:
                response = s.get(start_url.format(str(since)),headers=headers,timeout=3)
                res_data = response.json()
                if res_data["status"] == 1:
                    data = res_data["data"]  # 获取Data数组
                    time.sleep(0.5)
                ## 数据处理
                since = data[-1]["since"]  # 获取20条数据的最后一条json数据中的since
                ret = json_handle(data)   # 代码实现在下面
                try:
                    print(ret)
                    collection.insert_many(ret)   # 批量出入数据库
                    print("上述数据插入成功！！！！！！！！")
                except Exception as e:
                    print("插入失败")
                    print(ret)

                ##
        except Exception as e:
            print("!",end="异常，请注意")
            print(e,end=" ")
    else:
        print("循环完毕")

# 对JSON数据进行处理
def json_handle(data):
    # 提取关键数据
    list_infos = []
    for item in data:
        item = item["item_detail"]
        try:
            avatar = item["avatar"] # 用户头像
            item_id = item["item_id"] # 图片详情页面
            like_count = item["like_count"] # 喜欢数目
            pic_num = item["pic_num"] if "pic_num" in item else 0 # 图片总数
            reply_count =item["reply_count"]
            share_count =item["share_count"]
            uid = item["uid"]
            plain = item["plain"]
            uname = item["uname"]
            list_infos.append({"avatar":avatar,
                               "item_id":item_id,
                               "like_count":like_count,
                               "pic_num":pic_num,
                               "reply_count":reply_count,
                               "share_count":share_count,
                               "uid":uid,
                               "plain":plain,
                               "uname":uname})
        except Exception as e:
            print(e)
            continue
        return list_infos

