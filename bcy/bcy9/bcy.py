import requests
from index_mode import img_index
# https://blog.csdn.net/DHS2219576309/article/details/104677930?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522166712594216782428648786%2522%252C%2522scm%2522%253A%252220140713.130102334.pc%255Fall.%2522%257D&request_id=166712594216782428648786&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~first_rank_ecpm_v1~times_rank-10-104677930-null-null.142^v62^pc_search_tree,201^v3^control_1,213^v1^t3_esquery_v1&utm_term=%E7%88%AC%E8%99%AB%E7%88%AC%E5%8F%96%E5%8D%8A%E6%AC%A1%E5%85%83&spm=1018.2226.3001.4187
def get_data(uid,since,ture):
	url = 'https://bcy.net/apiv3/user/favor?uid='+uid+'&ptype=collect&mid='+uid+'&since='+since+'&size=35&_signature='+ture
	head = {
	'referer': 'https://bcy.net/u/4054592435529779/like/collect',
	'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3741.400 QQBrowser/10.5.3863.400',
	'x-requested-with': 'XMLHttpRequest',
	}
	response = requests.get(url,headers = head)
	json = response.json()
	return json


def json_index(since,ture,end):
	json = get_data(since,ture)
	like_list = json['data']['list']
	number = 0
	for data in like_list:   #遍历list中的元素
		number += 1
		item_id = data['item_detail']['item_id']
		url = 'https://bcy.net/item/detail/'+str(item_id)+'?_source_page=profile'
		img_index(url)
		if number == end:   #由于不是每次都需要将整个收藏夹中的信息都获取下来，所以设置了数量
			break
		else:
			pass



def main():
	uid = ''         #账号uid
	since = ''        #since的值
	ture = ''         #_signatrue的值
	end =              #结束数量
	json_index(uid,since,ture,end)

if __name__ == '__main__':
	main()
