import requests

def get_articles_by_name(public_account_name):
    # 构建请求的URL
    url = "https://api.weixin.qq.com/cgi-bin/token"

    # 设置请求参数
    params = {
        "grant_type": "client_credential",
        "appid": "wxb8acab815398b30f",
        "secret": "4348f3a48ab500b899512457b03699e0",
        'access_token': '70_fvVT9rRsb5FMvrljR_pee5vS3YM0k6H64yeJzXRm6iTkJFPRgvlDjgd4YEDEgXZDiyUkql3k1KUhJyFh-7T8hoOJ8oqpp1afXogFGpzRvan48sRA1MccdJHXc0kTEXbAFAKVO'
    }

    # 发送请求获取access_token
    response = requests.get(url, params=params)
    access_token = response.json()["access_token"]

    # 构建获取公众号信息的URL
    url = "https://api.weixin.qq.com/cgi-bin/account/getaccountbasicinfo"

    # 设置请求参数
    params = {
        "access_token": access_token
    }

    # 设置请求体
    data = {
        "account_list": [
            {
                "account_name": public_account_name
            }
        ]
    }

    # 发送请求获取公众号信息
    response = requests.post(url, params=params, json=data)
    account_info = response.json()["account_info"][0]

    # 获取公众号的fakeid
    fakeid = account_info["fakeid"]

    # 构建获取公众号文章列表的URL
    url = "https://api.weixin.qq.com/cgi-bin/appmsg"

    # 设置请求参数
    params = {
        "access_token": access_token
    }

    # 设置请求体
    data = {
        "fakeid": fakeid
    }

    # 发送请求获取公众号文章列表
    response = requests.post(url, params=params, json=data)
    article_list = response.json()["app_msg_list"]

    # 输出文章标题和链接
    for article in article_list:
        title = article["title"]
        link = article["link"]
        print(f"标题：{title}")
        print(f"链接：{link}")
        print()

# 输入公众号名称
public_account_name = input("请输入公众号名称：")

# 获取公众号文章列表并打印
get_articles_by_name(public_account_name)
