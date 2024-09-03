import requests
from bs4 import BeautifulSoup
# https://blog.csdn.net/m0_48405781/article/details/108813927?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522166712594216782428648786%2522%252C%2522scm%2522%253A%252220140713.130102334.pc%255Fall.%2522%257D&request_id=166712594216782428648786&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~first_rank_ecpm_v1~times_rank-21-108813927-null-null.142^v62^pc_search_tree,201^v3^control_1,213^v1^t3_esquery_v1&utm_term=%E7%88%AC%E8%99%AB%E7%88%AC%E5%8F%96%E5%8D%8A%E6%AC%A1%E5%85%83&spm=1018.2226.3001.4187
album_urls = []  # 相册url列表

headers = {
    "Host": "bcy.net",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:63.0) Gecko/20100101 Firefox/63.0"
}


# 获取相册url
class AlbumUrl():

    def __init__(self, url, url2):
        self.url = url
        self.url2 = url2

    def page(self, start, end):

        for i in range(start, end):

            url = self.url % i
            response = requests.get(url, headers=headers)

            response.encoding = 'utf-8'
            after_bs = BeautifulSoup(response.text, 'lxml')

            li_s = after_bs.find_all('li', class_='js-smallCards _box')  # 提取li标签内容

            for li in li_s:
                list_a = li.find_all('a', class_='db posr ovf')  # 提取a标签内容
                for a in list_a:
                    a_href = a.get('href')  # 取出部分url 进行拼接
                    album_urls.append(self.url2 + a_href)


if __name__ == '__main__':
    url = 'https://bcy.net/coser/index/ajaxloadtoppost?p=%s'
    url2 = 'https://bcy.net'
    spider = AlbumUrl(url, url2)
    spider.page(1, 6)  # 分析出来的页数