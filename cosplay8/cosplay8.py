import re

import parsel  # 解析数据 工具
import requests  # 发送请求

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36'
}
for page in range(1, 7):
    url = f'http://www.cosplay8.com/pic/xiezhen/list_224_{page}.html'
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    # <Response [200]>: 响应成功
    #   a. 结构化数据
    #       json
    #   b. 非结构化数据
    #       html
    html_data = response.text
    # <div></div>  <a></a> <p></p> <img />
    selector = parsel.Selector(html_data)
    # ::attr(href): 获取到 标签属性为href内容
    url_list = selector.css('.txtover::attr(href)').getall()
    title_list = selector.css('.txtover::attr(title)').getall()
    zip_data = zip(title_list, url_list)
    for title, sub_url in zip_data:
        # link = '网址' + sub_url
        link = 'http://www.cosplay8.com' + sub_url
        print(title, link)
        response_1 = requests.get(link, headers=headers)
        response_1.encoding = 'utf-8'
        html_data_1 = response_1.text
        page_num = re.findall('共(.*?)页', html_data_1)[0]
        selector_1 = parsel.Selector(html_data_1)
        # id选择器
        sub_img = selector_1.css('#bigimg::attr(src)').get()
        img_list = []
        # img_url_ = '网址' + sub_img
        img_url_ = 'http://www.cosplay8.com' + sub_img
        img_list.append(img_url_)
        for page in range(2, int(page_num) + 1):
            detail_sub = link.replace('.html', '')
            detail_url = detail_sub + '_' + str(page) + '.html'
            detail_html = requests.get(detail_url, headers=headers).text
            selector_2 = parsel.Selector(detail_html)
            # img_url_ = '网址'+selector_2.css('#bigimg::attr(src)').get()
            img_url_ = 'http://www.cosplay8.com'+selector_2.css('#bigimg::attr(src)').get()
            img_list.append(img_url_)
        print(img_list)
        for img_url in img_list:
            img_data = requests.get(img_url).content
            img_name = img_url.split('/')[-1]   # 标题分割取最后一个内容
            with open(f'img/{img_name}', mode='wb') as f:
                f.write(img_data)
