import concurrent.futures
import re
import time

import parsel
import requests


def change_title(title):
    mode = re.compile(r'[\\\/\:\*\?\"\<\>\|\n]')
    new_title = re.sub(mode, '_', title)
    return new_title


def get_response(html_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
    }
    response = requests.get(url=html_url, headers=headers)
    return response


def save(name, title, img_url):
    img_content = get_response(img_url).content
    with open('img\\' + title + '.' + name, mode='wb') as f:
        f.write(img_content)
        print('正在保存：', title)


def main(html_url):
    html_data = get_response(html_url).text
    selector = parsel.Selector(html_data)
    divs = selector.css('#container div.tagbqppdiv')
    for div in divs:
        title = div.css('img::attr(title)').get()
        img_url = div.css('img::attr(data-original)').get()
        name = img_url.split('.')[-1]
        new_title = change_title(title)
        if len(new_title) > 255:
            new_title = new_title[:10]
            save(name, new_title, img_url)
        else:
            save(name, new_title, img_url)


if __name__ == '__main__':
    start_time = time.time()
    exe = concurrent.futures.ThreadPoolExecutor(max_workers=7)
    for page in range(1, 201):
        url = f'https://www.fabiaoqing.com/biaoqing/lists/page/{page}.html'
        exe.submit(main, url)
    exe.shutdown()
    use_time = int(time.time()) - int(start_time)
    print(f'总计耗时：{use_time}秒')
