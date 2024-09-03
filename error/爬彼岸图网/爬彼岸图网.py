import requests
from lxml import etree
from fake_useragent import UserAgent
import os


class Pic(object):
    def __init__(self) -> None:
        self.url = 'https://pic.netbian.com'  # self.url网站链接
        ua = UserAgent().random
        self.header = {
            'user-agent': ua
        }
        self.fileName = './壁纸'
        if os.path.exists(self.fileName) == False:
            os.mkdir(self.fileName)

    # 运行
    def run(self):
        print('欢迎使用彼岸图网爬虫\n温馨提示: 请不要爬取过多内容，出现问题概不负责。\n')
        while True:
            self.ch_class()
            self.ch_way()
            q = input('爬取完成，输入"Q"退出程序，其他任意键继续...\n请输入: ')
            if q == 'q' or q == 'Q':
                break

    # 发送请求处理响应
    def send(self, page_url):
        res = requests.get(page_url, headers=self.header)
        html = etree.HTML(res.content.decode('gbk'))
        ls = html.xpath('//*[@id="main"]/div[3]/ul/li/a/@href')

        for i in ls:
            imgpage_url = self.url + i
            imgpage_res = requests.get(imgpage_url, headers=self.header)
            imgpage_html = etree.HTML(imgpage_res.content.decode('gbk'))
            img_ls = imgpage_html.xpath('//*[@id="img"]/img/@src')
            img_url = self.url + img_ls[0]
            tmp = img_ls[0].rfind('-')
            img_name = img_ls[0][tmp+1:]
            img = requests.get(img_url, headers=self.header)
            filename = self.fileName + '/' + img_name
            self.save_img(filename, img)
            print(f'{img_name}  爬取完成...')

    # 选择壁纸分类
    def ch_class(self):
        while True:
            ch = eval(input('请选择壁纸分类: \n' + '=='*20 +
                      '\n0. 默认\n1. 最新\n2. 4K动漫\n3. 4K美女\n4. 4K风景\n5. 4K游戏\n6. 4K影视\n' + '=='*20 + '\n请输入: '))
            if ch == 0:
                self.class_url = self.url  # self.class_url分类链接
                break
            elif ch == 1:
                self.class_url = self.url + '/new'
                self.fileName = self.fileName + '/最新'
                if os.path.exists(self.fileName) == False:
                    os.mkdir(self.fileName)
                break
            elif ch == 2:
                self.class_url = self.url + '/4kdongman'
                self.fileName = self.fileName + '/动漫'
                if os.path.exists(self.fileName) == False:
                    os.mkdir(self.fileName)
                break
            elif ch == 3:
                self.class_url = self.url + '/4kmeinv'
                self.fileName = self.fileName + '/美女'
                if os.path.exists(self.fileName) == False:
                    os.mkdir(self.fileName)
                break
            elif ch == 4:
                self.class_url = self.url + '/4kfengjing'
                self.fileName = self.fileName + '/风景'
                if os.path.exists(self.fileName) == False:
                    os.mkdir(self.fileName)
                break
            elif ch == 5:
                self.class_url = self.url + '/4kyouxi'
                self.fileName = self.fileName + '/游戏'
                if os.path.exists(self.fileName) == False:
                    os.mkdir(self.fileName)
                break
            elif ch == 6:
                self.class_url = self.url + '/4kyingshi'
                self.fileName = self.fileName + '/影视'
                if os.path.exists(self.fileName) == False:
                    os.mkdir(self.fileName)
                break
            else:
                ch = eval(input('序号错误，请重新输入: '))

    # 选择爬取方式
    def ch_way(self):
        ch = eval(input('请选择爬取类型: \n1.爬取第n页\n2.爬取前n页\n请输入: '))
        while True:
            if ch == 1:
                page = eval(input('你想爬取第几页: '))
                if page == 1:
                    page_url = self.class_url
                    self.send(page_url)
                else:
                    page_url = self.class_url + f'index_{page}.html'
                    self.send(page_url)
                break
            elif ch == 2:
                page = eval(input('你想爬取前几页: '))
                if page == 1:
                    page_url = self.class_url
                    self.send(page_url)
                else:
                    for i in range(page):
                        tmp = i + 1
                        if tmp == 1:
                            page_url = self.class_url
                            self.send(page_url)
                            # print(page_url)
                        else:
                            page_url = self.class_url + f'/index_{tmp}.html'
                            # print(page_url)
                            self.send(page_url)
                break
            else:
                ch = eval(input('序号错误，请重新输入: '))

    # 保存图片
    def save_img(self, filename, img):
        with open(filename, 'wb') as f:
            f.write(img.content)


pic = Pic()
pic.run()
