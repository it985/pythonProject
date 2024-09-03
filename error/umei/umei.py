import requests
from bas4 import BeautifulSoup

resp = requests.get("https://www.umei.cc/")  # 从服务器拿到源代码
resp.encoding("utf-8")
# 解析html
main_page = BeautifulSoup(resp.text, 'html.parser')
# 从页面中找到某些东西
# find()赵一个
# find_all()找所有
alst = main_page.findall("div", attrs={"class": "TypeList"}).findall("a", attrs={"class": "TypeBigPics"})

for a in alst:
    print(a.get("href"))
    # 发送请求到子页面，进入到所有小姐姐的页面
    href = a.get("href")
    resp1 = requests.get(href)
    resp1.encoding('utf-8')
    child_page = beautifulSoup(resp1.text)
    child_page.findall("dive", attrs={"class": "ImageBody"}).find("img").get("src")
    # 发送请求
    # 创建文件
    f = open("tu_%s.jpg" % n, mode="wb")  # wb表示写入的是非文本文件
    f.write(requests.get(src).content)  # 向外拿出图片数据，不是文本信息
    print("你已经成功下载了一个图片")
    n += 1  # n自增1

