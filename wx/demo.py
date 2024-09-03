import requests
import json

# 替换为你的AppID和AppSecret
app_id = 'wxb8acab815398b30f'
app_secret = '4348f3a48ab500b899512457b03699e0'
access_token ='70_fvVT9rRsb5FMvrljR_pee5vS3YM0k6H64yeJzXRm6iTkJFPRgvlDjgd4YEDEgXZDiyUkql3k1KUhJyFh-7T8hoOJ8oqpp1afXogFGpzRvan48sRA1MccdJHXc0kTEXbAFAKVO'

# 获取access_token
url = f'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={app_id}&secret={app_secret}'
response = requests.get(url)
access_token = json.loads(response.text)['access_token']

# 使用access_token进行其他操作...
