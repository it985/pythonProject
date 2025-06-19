# https://blog.csdn.net/jack_zj123/article/details/120082974?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522166702249316782427462704%2522%252C%2522scm%2522%253A%252220140713.130102334.pc%255Fblog.%2522%257D&request_id=166702249316782427462704&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~blog~first_rank_ecpm_v1~hot_rank-18-120082974-null-null.nonecase&utm_term=%E5%A5%97%E5%9B%BE%E5%90%A7%20%E7%88%AC%E8%99%AB&spm=1018.2226.3001.4450
'''
第一步：请求网页
'''
import requests
# 头标签
headers = {
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 Edg/92.0.902.84'
}

Get_url = requests.get('https://www.xrmn5.com/',headers=headers)
Get_url.encoding = 'utf-8'
print(Get_url.text)
print(Get_url.request.headers)
Get_html = Get_url.text
'''
第二步：解析网页
'''

import re
# 正则表达式对应的为：
# (.*?):获取（）内的所有
# \"(.*?)\" 用于匹配网页
# re.findall 用于获取（）内的数据并每存为元组
urls = re.findall('<li class="i_list list_n2"><a  href=\"(.*?)\" alt=(.*?) title=.*?><img src=\"(.*?)\"',Get_html)
patren1 = '<div class="postlist-imagenum"><span>(.*?)</span></div></a><div class="case_info"><div class="meta-title">\[.*?\](.*?)</a></div>'
patren2 = '<div class="meta-post"><i class="fa fa-clock-o"></i>(.*?)<span class="cx_like"><i class="fa fa-eye"></i>(.*?)</span>'
inforName = re.compile(patren1,re.S).findall(Get_html)
likeNum = re.compile(patren2,re.S).findall(Get_html)
'''
第三步：存储封面
'''
import os
import time

dir = r"E:/itheima149/code/com/pythonProject/xrmn5/PythonGet/"
url = "https://pic.xrmn5.com"
# 创建目录：人名+时间+专辑名
num = len(likeNum)
for i in range(num):
	if (int(likeNum[i][1]) > 500):
		getImgDir=dir+str(inforName[i][0])+'/'+str(likeNum[i][0])+'/'+str(inforName[i][1]+'/')
		# 创建对应目录
		if not os.path.exists(getImgDir):
			os.makedirs(getImgDir)
		imgUrl = url+urls[i][2]
		imgName = getImgDir+urls[i][2].split('/')[-1]
		print(imgName)
		time.sleep(1)
		# 获取封面图片
		Get_Img = requests.get(imgUrl, headers=headers)
		with open(imgName,'wb') as f:
			f.write(Get_Img.content)
		# 进入具体网页
