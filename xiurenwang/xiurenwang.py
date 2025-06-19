import os

import requests
from lxml import etree


class XiuPeople():
    # 初始化方法
    def __init__(self):
        # url
        self.url = 'https://www.xiurenwang.vip/bang?f=2'
        # headers
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
        }

    # 发送请求获取数据
    def get_data(self):
        response = requests.get(url=self.url, headers=self.headers)
        # 返回响应
        return response

    # 获取页面列表链接
    def parse_list(self, response):
        html = etree.HTML(response.content)
        # 每一个a列表链接
        node_list = html.xpath('//div[@class="list"]/li/a/@href')
        # 文件名列表
        name_list = html.xpath('//div[@class="tit"]/a/text()')
        # name_list = html.xpath('')
        li_list = list()
        for node in node_list:
            # 拼接url
            node_link = 'https://www.xiurenwang.vip/' + node
            # 将每个连接添加到列表返回
            li_list.append(node_link)
        # 返回列表url和文件名字
        return li_list, name_list

    # 内页解析
    def parse_detail(self, li_list):
        # 遍历列表
        img_list = list()
        for li in li_list:
            self.url = li
            response = self.get_data()
            html = etree.HTML(response.content)
            img_node = html.xpath('//div[@id="image"]/a/@href')
            for img_link in img_node:
                # 循环将每个图片链接放入列表
                img_list.append(img_link)
                print(img_link)
        return img_list

    #  保存数据
    def save_data(self, img_list, name_list):
        # 循环每个文件名
        for name in name_list:
            # 循环每个图片链接
            for link in img_list:
                title = str(link).split("/")[-1].split(".")[0]
                # 去除文件命中/,与路径冲突
                stitle = str(name).replace('/', '')
                add_title = stitle + title
                self.url = link
                response = self.get_data()
                # 保存数据
                with open("./picture/" + add_title + '.jpg', "wb") as f:
                    f.write(response.content)

    # 翻页
    def next_page(self):
        for i in range(2,241):
            next_url = 'https://www.xiurenwang.vip/bang/page/{}?f=2'.format(i)
            self.url = next_url
            print(self.url)
            response = self.get_data()
            li_list, name_list = self.parse_list(response)
            img_list = self.parse_detail(li_list)
            self.save_data(img_list, name_list)
            self.next_page()
            if i > 241:
                break

    # 调用
    def run(self):
        response = self.get_data()
        li_list, name_list = self.parse_list(response)
        img_list = self.parse_detail(li_list)
        self.save_data(img_list, name_list)
        self.next_page()


if __name__ == '__main__':
    try:
        os.mkdir("./picture")
    except:
        print("文件夹已新建")
    xiu = XiuPeople()
    xiu.run()

