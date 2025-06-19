import re

import pymongo
from pyquery import PyQuery as pq

client=pymongo.MongoClient(host='localhost',port=27017)
table=client.taobao.mei


def save_to_mongo(result):
	try:
		if table.insert(result):
			print('存储到Mongo成功')
	except Exception:
		print('存储到Mongo失败',result)

def father_link():
	for i in range(1,43):
		doc=pq(url='http://www.umei.cc/meinvtupian/rentiyishu/'+str(i)+'.htm',encoding='utf-8')
		items=doc('.TypeList li').items()
		for item in items:
			Son_link=item.find('a').attr('href')
			doc2=pq(Son_link,encoding='utf-8')
			#下载第一页图片
			image_url1=doc('#ArticleId22 > p > a > img').attr('src')
			image1={'image':image_url1}
			save_to_mongo(image1)
			print('save number 1 success!')
			page_num=doc2('body > div.wrap > div.NewPages > ul > li:nth-child(1) > a').text()
			page_num=re.findall(r"\d+\.?\d*",page_num)
			try:
				page_num=int(page_num[0])
				for l in range(2,page_num):
					Son_url=Son_link[:-4]+'_'+str(l)+'.htm'
					doc3=pq(Son_url,encoding='utf-8')
					image_url=doc3('#ArticleId22 > p > a > img').attr('src')
					image={'image':image_url}
					save_to_mongo(image)
					print('save success!')
			except Exception:
				pass


def main():
	father_link()


if __name__ == '__main__':
	main()
