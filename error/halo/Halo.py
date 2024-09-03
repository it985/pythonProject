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
# 1获取归档目录下的所有文章链接，2获取你的token，3解析文章url获取html，4将html转换为md，5上传文章
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
