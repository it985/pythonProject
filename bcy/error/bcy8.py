import datetime
import requests
import json
import re
import osdef
# https://blog.csdn.net/qq_54245135/article/details/124286242?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522166712594216782428648786%2522%252C%2522scm%2522%253A%252220140713.130102334.pc%255Fall.%2522%257D&request_id=166712594216782428648786&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~first_rank_ecpm_v1~times_rank-5-124286242-null-null.142^v62^pc_search_tree,201^v3^control_1,213^v1^t3_esquery_v1&utm_term=%E7%88%AC%E8%99%AB%E7%88%AC%E5%8F%96%E5%8D%8A%E6%AC%A1%E5%85%83&spm=1018.2226.3001.4187
get_res(url):  # 网页请求，当错误过多则跳过此链接
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36',
    # 'cookie':'',#如果自己的喜欢设置了只能自己看，那就填写自己的cookie
}
count = 0
while True:
    count += 1
    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.encoding = 'utf-8'
    except:
        pass
    else:
        if res.status_code == 200:
            return res
        if count >= 10:
            return Falsedef
            first_favor_page(uid):  # 我的喜欢第一个页面，前35个喜欢
url = 'https://bcy.net/u/' + uid + '/like'
res = get_res(url)
pattern = 'window.__ssr_data = JSON.parse\("(.*?)"\);\n      window._UID_ ='
text = re.findall(pattern, res.text)[0].replace('\\"', '"').replace('u002F', '').replace('\\\\', '/')
item_id = re.findall('"item_id":"(.*?)"', text)
urls = []
for i in range(len(item_id)):
    urls.append('https://bcy.net/item/detail/' + item_id[i] + '?_source_page=profile')
return urlsdef
all_favor_page(url):  # 获取我的喜欢所有页面，35个喜欢为一个喜欢页面
uid = re.findall('uid=(.*?)&ptype=', url)[0]
try:
    urls = first_favor_page(uid)
    while True:
        print(url)
        res = get_res(url)
        List = res.json()['data']['list']
        item_id_list = []
        since_list = []
        for i in range(len(List)):
            item_id_list.append(
                'https://bcy.net/item/detail/' + List[i]['item_detail']['item_id'] + '?_source_page=profile')
            since_list.append(List[i]['since'])
        urls = urls + item_id_list
        url = 'https://bcy.net/apiv3/user/favor?uid=2448850&ptype=like&mid=2448850&since=' + since_list[-1] + '&size=35'
except:
    return urls


def get_label(res):  # 获取一个图集的标签
    text1 = re.findall('<div class="tag-group">(.*?)</div>', res.text)[0]
    text2 = re.findall('<span>(.*?)</span></a>', text1)
    label = ' '.join(text2)
    file_pattern = '\/:.?"<>|'
    for pat in file_pattern:
        label = label.replace(pat, '')
    return label


def download(url, path):  # 下载图集链接下的图片
    if not os.path.exists(path):
        os.mkdir(path)
    res = get_res(url)
    t = re.findall('<div class="meta-info mb20"><span>(.*?)</span>', res.text)[0].split(' ')[0]  # 图集发布时间
    label = get_label(res)
    try:
        pattern = 'window.__ssr_data = JSON.parse\("(.*?)"\);\n      window._UID_ ='
        target_data = re.findall(pattern, res.text)[0].replace('\\"', '"').replace('u002F', '').replace('\\\\', '/')
    except:
        pass
    else:
        target_img_data = json.loads(target_data, strict=False)['detail']['post_data']['multi']
        num = len(os.listdir(path))
        i = 0
        print("-----开始下载！------")
        for img_data in target_img_data:
            img_url = img_data['original_path']
            if img_url.find('jpg') >= 0:
                img_fomat = '.jpg'
            elif img_url.find('png') >= 0:
                img_fomat = '.png'
            elif img_url.find('gif') >= 0:
                img_fomat = '.gif'
            else:
                img_fomat = '.jpg'
            num += 1
            i += 1
            name = str(datetime.date.today()) + '(' + str(num) + ')' + '[' + t + ']' + '[' + label + ']' + img_fomat
            print("下载进程：{}/{}   文件名：{}    已下载数目：{}    ".format(i, len(target_img_data), name, num), end='')
            print("文件路径：", path)
            img_content = get_res(img_url).content
            with open(path + "/" + name, 'wb') as f:
                f.write(img_content)
        print("-----下载完成！------")

        def main(url, path):
            page_url_list = all_favor_page(url)
            Len = len(page_url_list)
            page_url_list = page_url_list[::-1]
            for i in range(Len):  # 单线程，如果觉得下载慢，可以把for循环弄成多线程
                print('我的喜欢页面获取超链接进程：{}/{}'.format(i + 1, Len))
                try:
                    print(page_url_list[i])
                    download(page_url_list[i], path + "//")
                except:
                    pass

        if __name__ == '__main__':
            # 如果我的喜欢设置了只能自己看，就在get_res(url)中填写自己的cookie
            path = 'D://bcy'  # 保存路径，文件夹自己会生成
            url = ''  # 填写请求网址
            main(url, path)
