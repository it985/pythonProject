import requests
import parsel   # lxml  re  bs4
import re
import os

headers = {
    'referer': 'https://www.jdlingyu.com/tuji',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
}

for page in range(1, 393):
    url = f'https://www.jdlingyu.com/tuji/page/{page}'
    response = requests.get(url, headers=headers)
    # <Response [200]>: 请求成功
    html_data = response.text
    # re
    # url_list = re.findall('<h2><a  target="_blank" href="(.*?)">.*?</a></h2>', html_data)
    # xpath
    selector = parsel.Selector(html_data)
    url_list = selector.xpath('//div[@class="post-info"]/h2/a/@href').getall()
    for detail_url in url_list:
        detail_html = requests.get(detail_url, headers=headers).text
        detail_selector = parsel.Selector(detail_html)
        title = detail_selector.xpath('//h1/text()').get()
        # 如果不存在 img/title
        if not os.path.exists('img/' + title):
            # 那就新建
            os.mkdir('img/1' + title)
        img_list = detail_selector.xpath('//div[@class="entry-content"]//img/@src').getall()
        for img in img_list:
            # 获取二进制数据
            img_data = requests.get(img, headers=headers).content
            img_title = img.split('/')[-1]
            with open(f'img/{title}/{img_title}', mode='wb') as f:
                f.write(img_data)
            print(f'正在爬取: {img_title}')

