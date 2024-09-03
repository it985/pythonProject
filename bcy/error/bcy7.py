import httpx
import chompjs
import json
import fuckit
import re
import os
from faker import Faker
# https://blog.csdn.net/weixin_46913162/article/details/124747821?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522166712594216782428648786%2522%252C%2522scm%2522%253A%252220140713.130102334.pc%255Fall.%2522%257D&request_id=166712594216782428648786&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~first_rank_ecpm_v1~times_rank-3-124747821-null-null.142^v62^pc_search_tree,201^v3^control_1,213^v1^t3_esquery_v1&utm_term=%E7%88%AC%E8%99%AB%E7%88%AC%E5%8F%96%E5%8D%8A%E6%AC%A1%E5%85%83&spm=1018.2226.3001.4187
def get_url_list():
    """构建url列表

    Returns:
        _type_: _description_
    """
    return [page_url.format(i) for i in range(1, 2)]

def parse_url(url):
    """发送请求，获取响应数据

    Args:
        url (_type_): _description_

    Returns:
        _type_: _description_
    """
    with httpx.Client() as s:
        r = s.get(url, headers=headers)
        return r.content.decode()
def get_img_ids(json_str):
    """提取出每张图片的id

    Args:
        json_str (_type_): _description_

    Yields:
        _type_: _description_
    """
    json_datas = json.loads(json_str)
    for json_data in json_datas.get('data').get('top_list_item_info'):
        # 提取图片id
        yield {'img_id': json_data.get('item_detail').get('item_id')}
def get_pic_url(html_str):
    """获取图片的真实url地址

    Args:
        html_str (_type_): _description_

    Returns:
        _type_: _description_
    """
    pattern = 'window.__ssr_data = JSON.parse\("(.*?)"\);'
    with fuckit:
        json_str = re.search(pattern, html_str, re.S).group(1).replace('\\', '')
        json_data = chompjs.parse_js_object(json_str)
        img_url_temp = json_data.get('detail').get('post_data').get('multi')[0].get('origin')
        pic_url = re.sub('u002F', '/', img_url_temp)
        return pic_url
def down_pic(pic_url):
    """保存图片

    Args:
        pic_url (_type_): _description_
    """
    f = Faker(locale='zh_CN')
    pic_name = f.random_number(digits=8)
    path = os.path.join('cos_img', f'{pic_name}.jpg')
    r = httpx.get(pic_url, headers=headers)
    with open(path, 'wb') as f:
        f.write(r.content)
        print(f'{pic_name}爬取成功......!!!')
def main():
    """实现程序的主要逻辑思路
    """
    # 1.构建url列表
    url_list = get_url_list()
    for url in url_list:
        # 2.发送请求，获取响应数据
        json_str = parse_url(url)
        # 3.提取图片id
        img_ids = get_img_ids(json_str)
        for img_id in img_ids:
            # 4.构建图片的链接地址
            img_url = img_url_temp.format(img_id.get('img_id'))
            # 5.对图片链接发送请求
            html_str = parse_url(img_url)
            # 6.提取图片真实的地址
            pic_url = get_pic_url(html_str)
            # 7.保存图片
            down_pic(pic_url)
