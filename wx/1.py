import requests

access_token ='70_fvVT9rRsb5FMvrljR_pee5vS3YM0k6H64yeJzXRm6iTkJFPRgvlDjgd4YEDEgXZDiyUkql3k1KUhJyFh-7T8hoOJ8oqpp1afXogFGpzRvan48sRA1MccdJHXc0kTEXbAFAKVO'
def get_articles_url(public_account_name):
    # 构建请求的URL
    url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wxb8acab815398b30f&secret=4348f3a48ab500b899512457b03699e0"

    # 发送请求获取access_token
    response = requests.get(url)
    print(response.json())  # 打印返回的JSON数据
    access_token = response.json()["access_token"]

    # 构建获取公众号信息的URL
    url = f"https://api.weixin.qq.com/cgi-bin/account/getaccountbasicinfo?access_token=70_fvVT9rRsb5FMvrljR_pee5vS3YM0k6H64yeJzXRm6iTkJFPRgvlDjgd4YEDEgXZDiyUkql3k1KUhJyFh-7T8hoOJ8oqpp1afXogFGpzRvan48sRA1MccdJHXc0kTEXbAFAKVO"

    # 发送请求获取公众号信息
    response = requests.get(url, json={"account_list": [{"account_name": public_account_name}]}).json()

    # 获取公众号的fakeid
    fakeid = response["account_info"][0]["fakeid"]

    # 构建获取公众号文章列表的URL
    url = f"https://api.weixin.qq.com/cgi-bin/appmsg?access_token=70_fvVT9rRsb5FMvrljR_pee5vS3YM0k6H64yeJzXRm6iTkJFPRgvlDjgd4YEDEgXZDiyUkql3k1KUhJyFh-7T8hoOJ8oqpp1afXogFGpzRvan48sRA1MccdJHXc0kTEXbAFAKVO"

    # 发送请求获取公众号文章列表
    response = requests.post(url, json={"fakeid": fakeid}).json()

    # 获取所有文章链接
    article_urls = []
    if response["app_msg_cnt"] > 0:
        for article in response["app_msg_list"]:
            article_urls.append(article["link"])

    return article_urls


# 输入公众号名称
public_account_name = input("请输入公众号名称：")

# 获取所有文章链接
article_urls = get_articles_url(public_account_name)
print(f"公众号文章链接：")
for url in article_urls:
    print(url)
