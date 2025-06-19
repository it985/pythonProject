# 目标 ：https://www.bcy.net/item/detail/7086637143778401318
import asyncio
import os
import re
import time

import aiohttp
import js2py
import requests
import ua
from bs4 import BeautifulSoup

error_src_list = list()


def get_img_src(url):
    response = requests.get(url, headers=ua.headers())
    response.encoding = 'utf-8'
    html = response.text
    soup = BeautifulSoup(html, 'lxml')
    title = check_title(soup.find('title').string)
    script = 'var window = Object();%s;function show(){return window.__ssr_data}' % soup.find_all('script')[-5].string
    js = js2py.EvalJs()
    js.execute(script)
    result = js.show()
    img_src_list = [i['original_path'] for i in result['detail']['post_data']['multi']]
    return [title, img_src_list]
"""
get_img_src(url)
获取网页源代码
BeautifulSoup()解析网页
script 重构js代码
运行js代码{
	可以使用的方法：
		1.调用node.js ：麻烦
		2.使用execjs库 ：问题：兼容性不佳，编码问题，速度慢
		3.使用js2py库：问题：兼容性不佳， 速度中等
		......
		还有很多 自己搜索
}
"""


def check_title(title):
    rep = re.compile(r'[\\/:*?"<>|\r\n]+')
    change_name = rep.findall(title)
    if change_name:
        name = ''
        for i in change_name:
            name = title.replace(i, "_")
        return name
    else:
        return title
"""
check_title(title)
修改标题
正则查找，遍历修改
"""


async def download_img(session, url, path):
    async with semaphore:
        async with session.get(url, headers=ua.headers()) as response:
            if response.status == 200:
                with open(path, 'wb') as f:
                    while True:
                        buffer = await response.content.read(4096)
                        if not buffer:
                            break
                        f.write(buffer)
                        f.flush()
                    print('成功 : ' + url)
            else:
                print('失败 : ' + url)
                error_src_list.append([url, path])
"""
def download_img(session, url, path)
异步函数不会的自学
"""


async def run_tasks(task_list):
    async with aiohttp.ClientSession() as session:
        title = task_list[0]
        try:
            os.mkdir(f'./img/{title}')
        except os.error:
            pass
        urls = task_list[1]
        tasks = [download_img(session, url, './img/{}/{}.jpg'.format(title, p)) for p, url in enumerate(urls)]
        await asyncio.wait(tasks)
"""
run_tasks(task_list)
异步函数
aiohttp库重点
异步中无法使用requests库
不会的自学
"""


def error_download(url, path):
    response = requests.get(url, headers=ua.headers(), stream=True)
    if response.status_code == 200:
        with open(path, 'wb') as f:
            for data in response.iter_content(4096):
                f.write(data)
                f.flush()
        print('重试成功 : ' + url)
    else:
        time.sleep(5)
        error_download(url, path)
"""
error_download(url, path)
失败后重新下载
异步高并发，同时请求大量数据会失败
失败后添加到error_src_list列表异步协程任务完成后调用普通下载
"""


def main(url):
    tasks_list = get_img_src(url)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_tasks(tasks_list))
    for url, path in error_src_list:
        error_download(url, path)
"""
main()
获取任务列表运行协程任务
"""

if __name__ == '__main__':
    semaphore = asyncio.Semaphore(50) # 控制任务并发数
    main('https://www.bcy.net/item/detail/7086637143778401318')
