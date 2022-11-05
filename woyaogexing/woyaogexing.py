# python爬取网站上1000张唯美图片
import requests
from bs4 import BeautifulSoup
path='https://www.woyaogexing.com/tupian/weimei'  #爬取网站URL
p='https://www.woyaogexing.com'; #初始路径
path_all=[path]
for i in range(2,6):
    path_all.append(path+'/index_'+str(i)+'.html')  #所有的爬取页面
print(path_all) #打印所有的待爬取页面链接


l=[] # l储存一级套图页面url
def find_path(path):
    resp=requests.get(path)
    resp.encoding='utf-8'
    main_page=BeautifulSoup(resp.text,"html.parser")
    list=main_page.find_all("a", attrs={"class":"img"})  #直接找套图元素
    for ele in list:
        l.append(p+ele.get("href"))


fig=[]; #fig储存有所二级页面(JEPG)的URL
def find_fig(path):
    resp = requests.get(path)
    resp.encoding = 'utf-8'
    main_page = BeautifulSoup(resp.text, "html.parser")
    list = main_page.find_all("a", attrs={"class": "swipebox"})  # 直接找图片jpeg
    for p in list:
        fig.append(p.get("href"))

## 构建l和fig
for ele in path_all:  #构建l
    find_path(ele)
print(l)

for ele in l:      #构建fig
    find_fig(ele)
print(len(fig)) #fig储存图片的链接


# 下载图片并保存图片到指定文件夹
for i in range(len(fig)):
    f=open('./'+str(i)+'.jpeg',mode='wb') #在当前文件夹中创建文并保存
    f.write(requests.get('http:'+fig[i]).content)
    print('Successful '+str(i))

