import requests
from lxml import etree

headers = {

    'Cookie': 'Hm_lvt_c8263f264e5db13b29b03baeb1840f60=1632291839,1632373348; Hm_lpvt_c8263f264e5db13b29b03baeb1840f60=1632373697',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'}

for i in range(2, 3):
    url = f'https://www.3gbizhi.com/meinv/xgmn_{i}.html'
    response = requests.get(url, headers=headers)
    html = etree.HTML(response.text)
    href_list = html.xpath('//div[@class="contlistw mtw"]//ul[@class="cl"]/li/a/@href')
    title_list = html.xpath('//div[@class="contlistw mtw"]//ul[@class="cl"]/li/a/@title')
    for href, title in zip(href_list, title_list):
        res = requests.get(href, headers=headers)
        html_data = etree.HTML(res.text)
        img_url_list = html_data.xpath('//div[@class="picimglist pos"]/ul/li/a/img/@src')
        print(img_url_list)
        num = 0
        for img_url in img_url_list:
            img_url = ''.join(img_url.split('thumb_200_0_'))
            result = requests.get(img_url, headers=headers).content
            with open('xgmn/' + title + str(num) + '.jpg', 'wb')as f:
                f.write(result)
            num += 1
            print(f'正在下载{title}第{num}张！！！！')