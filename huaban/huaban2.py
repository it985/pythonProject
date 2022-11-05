import urllib.request
import re
import os
import datetime
import easygui


# 获取网页
def get_html(url):
    page = urllib.request.urlopen(url)
    html = page.read().decode('utf-8')  # 需要解码
    return html


# 下载图片
def get_image(path, html):
    # 获取HTML源码里面的app.page["pins"]部分，主要图片ID位于此部分
    get_app_page_pins = re.compile(r'app\.page\["pins"\].*?;', re.S)
    get_str = re.findall(get_app_page_pins, html)[0]

    pin_id = r'"pin_id":(\d+)'
    pin_id_re = re.compile(pin_id)

    # 获取图片ID，保存在列表中
    id_list = re.findall(pin_id_re, get_str)

    x = 0
    for pinId in id_list:
        # 获取跳转网页网址
        url_str = r'http://huaban.com/pins/%s/' % pinId
        # 获取点击图片时弹出网页的源码
        pinId_source = get_html(url_str)
        # 解析源码，获取原图片的网址
        img_url_re = re.compile('main-image.*?src="(.*?)"', re.S)
        img_url_list = re.findall(img_url_re, pinId_source)
        try:
            img_url = 'http:' + img_url_list[0]
            urllib.request.urlretrieve(img_url, path + '\%s.jpg' % x)
        except:
            print("获取图片：%s失败，跳过，获取下一张。" % img_url)
            continue
        print("获取成功！%s" % img_url)
        x += 1
    print("保存图片成功！")


# 创建文件夹路径
def createPath():
    while True:
        print('选择你要保存的路径')
        path = easygui.diropenbox()

        filePath = path + "\\" + str(datetime.datetime.now().strftime('%Y-%m-%d %H.%M.%S'))

        isExists = os.path.exists(filePath)
        if not isExists:
            # 创建目录
            os.makedirs(filePath)
            print('%s创建成功！' % filePath)
            break
        else:
            print('%s已存在重新输入！' % filePath)
    return filePath


if __name__ == '__main__':
    html = get_html("http://huaban.com/favorite/beauty/")
    get_image(createPath(), html)  # 调用创建文件夹方法并返回文件夹路径和传入网址

