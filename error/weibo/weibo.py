# 爬取微博 Duebass的图片
# https://blog.csdn.net/qq_21963133/article/details/90142087?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522166701693016782412587689%2522%252C%2522scm%2522%253A%252220140713.130102334.pc%255Fblog.%2522%257D&request_id=166701693016782412587689&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~blog~first_rank_ecpm_v1~hot_rank-21-90142087-null-null.nonecase&utm_term=%E7%BE%8E%E5%A5%B3&spm=1018.2226.3001.4450
import re
import ssl
from urllib import request

file_path = '/error/weibo'
# http://wallpaper.apc.360.cn/index.php?c=WallPaper&a=getAppsByCategory&cid=6&start=6590&count=50
base_url = 'https://m.weibo.cn/api/container/getIndex?is_hot[]=1&is_hot[]=1&jumpfrom=weibocom&type=uid&value=1969308311&containerid=1076031969308311&page='

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
    'Accept': 'application/json, text/plain, */*',
    'Referer': 'https://m.weibo.cn/p/1005051969308311/photos?from=page_100505&from=page_100505&mod=TAB&mod=TAB&jumpfrom=weibocom'
}

context = ssl._create_unverified_context()

for i in range(5, 6):
    try:
        realurl = base_url + str(i)
        req = request.Request(url=realurl, headers=header)
        # resp = requests.get(realurl, headers=header)
        resp = request.urlopen(req, context=context).read().decode()
        print('==============正在下载第' + str(i) + '页的图片===============')
        # 先获取所有的large里面的url，注意观察，大图的url中都包含/large,那么我们获取所有的url然后过虐掉不包含/large的url就行了
        pat = '"url":"(.*?)"'
        list1 = re.compile(pat).findall(resp)
        list2 = filter(lambda url: url.find('/large') != -1, list1)
        list2 = list(list2)
        for j in range(0, len(list2) - 1):
            pic_url = list2[j].replace('\/', '/')
            request.urlretrieve(pic_url, file_path + str(i) + str(j) + '.jpg')
        print('============第' + str(i) + '页的图片下载完成===============')

    except Exception as error:
        print(error)