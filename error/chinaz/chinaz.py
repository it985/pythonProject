import os
import urllib.parse
import urllib.request

from lxml import etree


# 首页：http://sc.chinaz.com/tupian/xingganmeinvtupian.html
# 分页后：http://sc.chinaz.com/tupian/xingganmeinvtupian_3.html

def handle_request(url,page):
	#由于页面不规律，需要增加个判断
	# 首页：http://sc.chinaz.com/tupian/xingganmeinvtupian.html
	# 分页后：http://sc.chinaz.com/tupian/xingganmeinvtupian_3.html
	if page == 1:
		url=url.format('')
	else:
		url=url.format('_' + str(page))
	headers={
		'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
	}
	request=urllib.request.Request(url=url,headers=headers)
	return request

def downoad_image(image_src):
	dirpath='xingganmeinv'
	if not os.path.exists(dirpath):
		os.mkdir(dirpath)
	#搞个文件名
	filename=os.path.basename(image_src)
	filepath=os.path.join(dirpath,filename)
	headers={
		'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
	}
	request=urllib.request.Request(url=image_src,headers=headers)
	response=urllib.request.urlopen(request)
	with open(filepath,'wb') as fp:
		fp.write(response.read())

#解析内容，并下载图片
def parse_content(content):
	tree=etree.HTML(content)
	img_list=tree.xpath('//div[@id="container"]/div/div/a/img')
	for lt in img_list:
		#处理图片懒加载
		img_href=lt.xpath('.//@src2')[0].replace('_s.','.')
		img_title=lt.xpath('.//@alt')[0]
		print('正在下载图片：%s  ......'%img_title)
		#方法一：
		# downoad_image(img_href)
		#方法二：
		dirname='meinv'
		if not os.path.exists(dirname):
			os.mkdir(dirname)
		# 后缀
		s=os.path.splitext(img_href)[-1]
		#图片的名称
		filepath=dirname+'/'+img_title+s
		urllib.request.urlretrieve(img_href,filepath)

def main():
	url='http://sc.chinaz.com/tupian/xingganmeinvtupian{}.html'
	start_page=int(input('请输入起始页码：'))
	end_page=int(input('请输入结束页码：'))
	for page in range(start_page,end_page+1):
		print('开始下载第%s页所有图片，请稍等......'%page)
		request=handle_request(url,page)
		content=urllib.request.urlopen(request).read().decode()
		parse_content(content)

if __name__ == '__main__':
	main()
