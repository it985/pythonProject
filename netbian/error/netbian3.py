from pyquery import PyQuery as pq
import requests

url = 'http://pic.netbian.com/4kmeinv/'
html = requests.get(url=url).text
doc_1 = pq(html)  # 字符串初始化
data_s = doc_1('.slist .clearfix li a').items()  # 使用CSS选择器进行定位，定位节点过多，需要遍历一下
for list_s in data_s:
    image_url = 'http://pic.netbian.com/' + list_s.attr.href  # 提取a节点中的href属性，并得到一个新的链接
    image = requests.get(image_url).text  # 访问第二个页面
    doc_2 = pq(image)  # 字符串初始化
    contents = 'http://pic.netbian.com/' + doc_2('#img img').attr.src  # 依然是CSS选择器，提取img节点的src属性
    print(contents)  # 打印链接结果
