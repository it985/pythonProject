# --*-- coding:utf-8 --*--
# @FileName : UtilHalo.py
# @Author   : Administrator
# @DateTime : 2022/10/27 10:20
# @Desc     : Halo博客爬虫相关工具类
# 导入模块
import json
import time

import markdownify
import parsel
import requests

headers = {
    'content-type': 'application/json'
}


def win_check_file_name(file_name: str) -> str:
    """
    检查文件名是否违规。如果违规，则处理后返回
    :param file_name: 文件名
    :return: 返回文件名
    """
    try:
        for i in ['/', '\\', ':', '*', '?', '<''>', '|']:
            if i in file_name:
                file_name = file_name.replace(i, '')
        return file_name
    except:
        file_name = str(time.time())
        return file_name


def format_html(html: str) -> str:
    """
    格式化 HTML 字符串，将 HTML 字符串文本转换为 Markdown 格式文本
    :param html: 需要转换的字符串文本
    :return: 返回 Markdown 格式文本
    """
    # 格式转换
    markdown = markdownify.markdownify(html).replace('> \n', '').replace('\n\n', '\n')
    return markdown

def get_token(username: str, password: str) -> str:
    """
    获取登录后的token
    :param username: 用户名
    :param password: 密码
    :return: 返回Token
    """
    url = 'https://blog.tryrun.top/api/admin/login'
    data = {
        'username': '2071916845@qq.com',
        'password': 'zx.2071916845',
    }
    token = json.loads(requests.post(url=url, headers=headers, data=json.dumps(data)).text)['data']['access_token']
    return token


def set_headers(token: str) -> dict:
    """
    生成请求头
    :param token: 登录后获取的Token
    :return: 返回生成后的请求头
    """
    headers = {
        'admin-authorization': token,
        'content-type': 'application/json'
    }
    return headers


def get_all_page(type: int) -> dict:
    """
    获取Halo前端页面信息
    :param type: 0 独立页面 1 自定义页面
    :return: 返回页面信息列表
    """
    if type:
        url = 'https://blog.tryrun.top/api/admin/sheets?page=0&size=100'
    else:
        url = 'https://blog.tryrun.top/api/admin/sheets/independent'
    res = requests.get(url=url, headers=headers)
    data = json.loads(res.text)['data']
    return data


def get_all_tags() -> dict:
    """
    获取所有标签
    :return: 返回标签数据
    """
    url = 'https://blog.tryrun.top/api/admin/tags?more=true'
    res = requests.get(url=url, headers=headers)
    data = json.loads(res.text)['data']
    return data


def get_all_categorie() -> dict:
    """
    获取所有分类目录
    :return: 返回分类目录数据
    """
    url = 'https://blog.tryrun.top/api/admin/categories'
    res = requests.get(url=url, headers=headers)
    data = json.loads(res.text)['data']
    return data


def add_tag(name: str, slug: str, thumbnail: str = None, color: str = None) -> dict:
    url = 'https://blog.tryrun.top/api/admin/tags'
    data = {
        "name": name,
        "slug": slug,
        "thumbnail": thumbnail,
        "color": color,
    }
    if thumbnail:
        data['thumbnail'] = thumbnail
    if color:
        data['color'] = color
    res = requests.post(url=url, headers=headers, data=json.dumps(data))
    return json.loads(res.text)


def add_categories(name: str, slug: str, parentId: str = None, thumbnail: str = None, password: str = None,
                   description: str = None) -> dict:
    """
    添加分类目录
    :param name: 分类目录名称
    :param slug: 分类目录别名
    :param parentId: 上级分类目录ID
    :param thumbnail: 分类目录封面
    :param password: 分类目录设置密码
    :param description: 分类目录说明
    :return: 返回响应数据
    """
    url = 'https://blog.tryrun.top/api/admin/categories'
    data = {
        "name": name,
        "slug": slug,
    }
    if parentId:
        data['parentId'] = parentId
    if thumbnail:
        data['thumbnail'] = thumbnail
    if password:
        data['password'] = password
    if description:
        data['description'] = description
    res = requests.post(url=url, headers=headers, data=json.dumps(data))
    return json.loads(res.text)


def add_archive(title: str, slug: str, originalContent: str, content: str, categoryIds: list = None,
                tagIds: list = None,
                summary: str = None, password: str = None, thumbnail: str = None, metaKeywords: str = None,
                metaDescription: str = None) -> dict:
    """
    将新文章写入到Halo
    :param title: 文章标题
    :param slug: 文章别名
    :param originalContent: 文章md格式字符串
    :param content: 文章html格式字符串
    :param categoryIds: 文章分类目录ID列表
    :param tagIds: 文章标签目录ID列表
    :param summary: 文章摘要
    :param password: 文章设置密码查看权限
    :param thumbnail: 文章封面图标
    :param metaKeywords: 文章SEO
    :param metaDescription: 文章SEO描述
    :return: 返回响应数据
    """
    url = 'https://blog.tryrun.top/api/admin/posts'
    data = {
        "title": title,
        "originalContent": originalContent,
        "content": content,
        "slug": slug,
        "status": "PUBLISHED",
        "keepRaw": True
    }
    if categoryIds:
        data['categoryIds'] = categoryIds
    if tagIds:
        data['tagIds'] = tagIds
    if summary:
        data['summary'] = summary
    if password:
        data['password'] = password
    if thumbnail:
        data['thumbnail'] = thumbnail
    if thumbnail:
        data['metaKeywords'] = metaKeywords
    if thumbnail:
        data['metaDescription'] = metaDescription
    res = requests.post(url=url, headers=headers, data=json.dumps(data))
    return json.loads(res.text)


def get_archives_url(url: str) -> list:
    """
    获取 halo 站点归档文章链接
    :param url: 站点 XML 链接
    :return: 返回所有文章 URL
    """
    # 获取站点xml
    html = requests.get(url).text

    u = 'https://' + url.split('/')[2]

    # 解析XML，获取站点URL
    _ = parsel.Selector(html).xpath('//*[@id="Joe"]/div/div/div/div/div/ul/li/div/ol/li/a/@href').getall()

    site_url = []

    for i in _:
        site_url.append(u + i)

    return site_url


def get_archives_html(url: str) -> str:
    """
    获取文章页面 HTML
    :param url: 文章页面 URL
    :return: 返回文章页面 HTML 字符串
    """
    html = requests.get(url).text
    html = str(parsel.Selector(html).xpath('//*[@id="Joe"]/div[2]/div/div[1]/div[2]/article/div').get())
    return html


if __name__ == '__main__':
    url = 'https://b.925i.cn/archives/'

    url_list = get_archives_url(url)

    for url in url_list:
        html = get_archives_html(url)
        md = format_html(html)
        file_name = url.split('/')[-1] + '.md'
        with open(file_name, 'w', encoding='utf-8') as f:
            f.writelines(md)
