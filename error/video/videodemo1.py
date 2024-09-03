# 导入数据请求模块
import requests  # pip install requests  win + R 输入cmd
# 导入正则
import re  # 内置模块 不需要大家去安装
import time  # 时间模块
from selenium import webdriver  # pip install selenium==3.141.0
def drop_down():
    """执行页面滚动的操作"""  # javascript
    for x in range(1, 30, 4):  # 1 3 5 7 9  在你不断的下拉过程中, 页面高度也会变的
        time.sleep(1)
        j = x / 9  # 1/9  3/9  5/9  9/9
        # document.documentElement.scrollTop  指定滚动条的位置
        # document.documentElement.scrollHeight 获取浏览器页面的最大高度
        js = 'document.documentElement.scrollTop = document.documentElement.scrollHeight * %f' % j
        driver.execute_script(js)


# 人怎么去操作浏览器的, 就怎么写代码...
# 1. 打开一个浏览器或者下载一个浏览器吧 创建浏览器对象(实例化一个浏览器对象)
driver = webdriver.Chrome()
# 2. 输入一个网址 请求网址
driver.get('你要爬取得作者主页链接')
driver.implicitly_wait(10)
# 3. 提取所有li标签 返回列表
# drop_down()
lis = driver.find_elements_by_css_selector('.ECMy_Zdt')
for li in lis:
    html_url = li.find_element_by_css_selector('a').get_attribute('href')
    print(html_url)
    #  1. 发送请求, 用python代码模拟浏览器去发送请求
    # url = '你爬取得单个视频得链接'
    # headers 作用 伪装python代码 伪装成浏览器 user-agent: 用户代理 浏览器基本身份标识  cookie 用于检测用户信息, 是否有登陆账号
    headers = {
        'cookie': '自己去复制一下',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36'
    }
    response = requests.get(url=html_url, headers=headers)  # <Response [200]> 表示的是响应对象 200状态码 请求成功
    # 2. 获取数据
    # print(response.text)  # 获取html字符串数据  服务器返回response响应文本数据
    # 3. 解析数据
    # findall 找到所有, 从什么哪里去找什么数据  正则匹配出来数据返回都是列表数据 [] 列表 [0] 取第一个元素
    title = re.findall('<title data-react-helmet="true">(.*?) - 抖音</title>', response.text)[0]
    video_url = re.findall('src(.*?)vr%3D%2', response.text)[0]
    # print(video_url)
    video_url = requests.utils.unquote(video_url).replace('":"', 'https:')  # 解码 并且使用replace字符串替换
    # print(title)
    # print(video_url)
    # 4. 保存数据 视频数据内容
    video_content = requests.get(url=video_url, headers=headers).content  # 对于视频播放地址发送请求,获取二进制数据内容
    with open('video\\' + title + '.mp4', mode='wb') as f:
        f.write(video_content)
    print(title, '保存完成')
