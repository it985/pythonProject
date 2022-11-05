
### 3.动手写一个爬虫

此部分参考下面的爬虫实战



## 爬虫实战

**步骤分析**

```
1.搭建开发环境 Python3.7 或 Anaconda(推荐) 和 pycharm
2.安装依赖包 requests,bs4,lxml
3.准备要爬取的网址 http://pic.netbian.com/index_5.html
4.准备用户代理 User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0
5.写爬虫
6.运行爬虫
```



### 1.搭建开发环境

```
下载Python3.7
https://www.python.org/downloads/
```

安装很简单,直接一直下一步即可,不再赘述

但是这里有个比较重要的步骤,安装好了以后,需要搭建虚拟环境

```
pip install virtualenv
```

以下为常用命令

```
# 创建虚拟环境
virtualenv env

# 激活虚拟环境
# 进入到env下面的Scripts文件夹(windows)或bin文件夹(Linux)
activate

# 退出虚拟环境
deactivate
```



```
下载Anaconda
# 清华镜像网址
https://mirror.tuna.tsinghua.edu.cn/anaconda/archive/
```

![1569567754578](assets/1569567754578.png)

点击下载即可,安装较简单,不再赘述

如果你装的是Anaconda,则可能需要使用以下命令

```
# 创建虚拟环境
conda create -n 虚拟环境名称 要安装的依赖包,至少一个

# 激活虚拟环境
conda activate 虚拟环境名称

# 退出虚拟环境
conda deactivate

# 查看虚拟环境列表
conda env list

# 删除虚拟环境
# 或者直接去envs下面删除对应的虚拟环境包也可以
conda remove -n 虚拟环境名称 --all
```



```
安装Pycharm
# 下载地址
http://www.jetbrains.com/pycharm/download/#section=windows

# 安装教程
https://www.runoob.com/w3cnote/pycharm-windows-install.html
```



### 2.安装依赖包

这里我用windows+anaconda+pycharm进行开发

```
# 创建一个爬虫虚拟环境
conda create -n spider1910 requests
```

```
# 然后用pycharm创建一个爬虫项目,选择创建的虚拟环境
# 位于anaconda安装目录的envs文件夹
```

![1569569434579](assets/1569569434579.png)

![1569569501127](assets/1569569501127.png)

创建项目后,打开终端

先切换到我们创建的虚拟环境

```
conda activate spider1910
# 查看已安装的包
pip freeze
```

![1569570064990](assets/1569570064990.png)



安装其他依赖

```
pip install lxml
pip install bs4
```

![1569570149933](assets/1569570149933.png)



### 3.准备要爬取的网址

```
# 浏览器打开以下网址,这里用火狐浏览器
http://pic.netbian.com/index_5.html
```



### 4.准备用户代理

```
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0
```

鼠标右键,查看元素

![1569569772529](assets/1569569772529.png)

点网络,`ctrl+r`刷新,然后随便点一个网址

![1569569814872](assets/1569569814872.png)

右侧,点显示原始请求头,赋值`User-Agent`

![1569569861845](assets/1569569861845.png)

### 5.写爬虫

```python
# _*_ coding:UTF-8 _*_
# 开发人员: 理想国真恵玩-张大鹏
# 开发团队: 理想国真恵玩
# 开发时间: 2019/9/27 15:39
# 文件名称: BianImgSpider.py
# 开发工具: PyCharm

import requests, os, time
from bs4 import BeautifulSoup


# 1.准备url和请求头
# 2.发送get,获取响应数据,转换为html
# 3.提取本页图片和下一页地址
# 4.保存图片
# 5.循环执行第三步操作
class BianImgSpider:
    def __init__(self, url, base_url='http://pic.netbian.com'):
        self.base_url = base_url
        self.url = url
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0"}
        self.has_next = True  # 判断是否有下一页

    def get_html(self):
        """
        获取url地址的html源码
        :return: html源码
        """
        response = requests.get(self.url, headers=self.headers)
        response.encoding = 'gbk'
        return response.text

    def get_imgs_next_url(self):
        """
        获取图片本页的图片列表和下一页的地址
        :return: 图片列表,下一页url
        """
        print("正在爬取网页:", self.url)
        html = self.get_html()
        # print(html)
        # exit()
        soup = BeautifulSoup(html, 'lxml')
        img_list = soup.select('.slist ul li a img')
        # print(img_list)
        # 提取图片的src,装进列表
        imgs = []
        for i in img_list:
            src = i['src']
            src = self.base_url + src
            # print(src)
            # exit()
            imgs.append(src)
        # 提取下一页
        try:
            # next_url = soup.select('.page > a:nth-child(13)')[0]
            # print(next_url['href'])
            # exit()
            # 找到page
            page = soup.select('.page')[0]
            # print(page, type(page))
            # 下一页是最后一个a
            # print(page.a)
            # print(page.contents)
            # print(page.contents[-1])
            href = page.contents[-1]['href']
            # print(href)
            next_url = self.base_url + href
            # print(next_url)
            return next_url, imgs
        except:
            print("没有下一页了")
            # 告知没有下一页了,方便操作
            self.has_next = False

    def save_img(self, imgs):
        """
        保存列表中的图片
        :param imgs: 图片列表
        :return: True
        """
        try:
            for img in imgs:
                # 提取图片名字
                # print(type(img))
                img_name = img.split('/')[-1]
                # print(img_name)
                # 设置图片保存地址
                save_path = 'imgs'
                if not os.path.exists(save_path):
                    os.mkdir(save_path)
                response = requests.get(img, headers=self.headers)
                # 获取图片流
                with open(save_path + "/" + img_name, 'wb') as f:
                    # 每次读写1M数据
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
                # exit()
            print("一个图片列表被保存成功")
            return True
        except:
            print("保存失败")
            return False

    def run(self):
        """
        运行爬虫,保存图片
        :return: 成功返回True,失败返回False
        """
        try:
            while self.has_next:
                next_url, imgs = self.get_imgs_next_url()
                # print(imgs)
                # print(next_url)
                # 保存图片
                self.save_img(imgs)
                # 将url改为下一页的url
                self.url = next_url
                # 文明爬取,每爬取一页,休息一秒钟,防止破坏服务器
                time.sleep(1)
            return True
        except:
            print("保存图片失败")
            return False


if __name__ == '__main__':
    spider = BianImgSpider('http://pic.netbian.com/index_5.html')
    spider.run()
```