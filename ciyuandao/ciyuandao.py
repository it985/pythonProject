# 导入数据请求模块  --> 第三方模块 需要 在cmd里面 pip install requests
import requests
# 导入数据解析模块  --> 第三方模块 需要 在cmd里面 pip install parsel
import parsel
# 导入正则模块 --> 内置模块 不需要安装
import re
# 导入文件操作模块 --> 内置模块 不需要安装
import os.path
# 构建翻页
for page in range(2, 450):
    # format 字符串格式化方法
    print(f'正在采集第{page}页的数据内容')
    # 确定请求url地址  <目录页>
    url=f'http://ciyuandao.com/photo/list/0-4-{page}'
    headers = {
        # 浏览器基本身份信息
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36'
    }
    response = requests.get(url=url, headers=headers)
    # <Response [200]>  表示请求成功了 响应对象
    print(response)
    selector = parsel.Selector(response.text)
    href = selector.css('.pics ul li .tits::attr(href)').getall()
    for index in href:
        index_url='http://ciyuandao.com'+index
        index_data = requests.get(url=index_url, headers=headers).text
        index_selector = parsel.Selector(index_data)
        img_url_list = index_selector.css('.talk_pic img::attr(src)').getall()
        title = index_selector.css('.border_bottom::text').get()
        new_title = title = re.sub(r'[\/:*?"<>|]', '', title)
        num = 1
        # 自动创建文件夹
        file = f'img\\{new_title}\\'
        # 如果没有这个文件夹
        if not os.path.exists(file):
            # 自动创建文件夹
            os.makedirs(file)
        # for循环遍历 提取列表元素
        for img_url in img_url_list:
            # 获取图片二进制数据
            img_content = requests.get(url=img_url, headers=headers).content
            # 保存图片
            with open(file + new_title + str(num) + '.jpg', mode='wb') as f:
                # 写入数据
                f.write(img_content)
                # 每次循环 +1
                num += 1
            print(title, img_url)
