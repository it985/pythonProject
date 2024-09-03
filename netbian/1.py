#美女壁纸下载
import requests
from bs4 import BeautifulSoup
myheader = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'}
urls = ['https://pic.netbian.com/4kmeinv/']#构造每页网址
all_url = [] #设置空列表
for k in range(2,6):                 #构造每页网址
    page = f'https://pic.netbian.com/4kmeinv/index_{k}.html'
    urls.append(page)
for url in urls:                    #由于每页网址上的图片画质很低所以这里选择先爬取每张图图片的超链接
    r = requests.get(url,headers=myheader)#请求网页
    r.encoding='GBK'                    #中文编码
    sp = BeautifulSoup(r.text,'lxml')   #解析网页
    tg=sp.select_one('div.slist').select('li') #查找网页源代码里的class属性为slist的div标签并同时找div标签中的li标签
    for t in tg:                              #构造循环提取图片超链接
        header = 'https://pic.netbian.com'
        pic_url = header + t.a.get('href')        #构造网址形式
        all_url.append(pic_url)                   #存入all_url列表中
        pic_allurl = []  # 对每张图片的网页进行分析并构造下载网址并爬取高质量图片
        for url in all_url:  # 遍历网址
            r = requests.get(url)  # 请求网页
            r.encoding = 'GBK'  # 用中文编码
            sp = BeautifulSoup(r.text, 'lxml')  # 解析网页
            tags = sp.select_one('#img')  # 查找id为img的标签并存入tags
            src = ('https://pic.netbian.com' + tags.img.get('src'))  # 提取tags标签里的scr属性
            title = tags.img.get('title')  # 提取tags标签里的title属性
            pic_allurl.append((title, src))  # 将构造好的网址和标题作为元组放进pic_allurl=[]
            import os

            if not os.path.exists('美女壁纸'):  # 如果不存在文件夹则创立文件夹
                os.mkdir('美女壁纸')
            for title, src in pic_allurl:  # 拆解元组
                r = requests.get(src, headers=myheader)  # 请求二进制图片
                fileanme = './美女壁纸/' + title + src.split('/')[-1]  # 构造名字 按斜线切开取最后一个元素 同时确定了文件后缀
                with open(fileanme, 'wb') as f:  # 新建文件
                    f.write(r.content)  # 写入