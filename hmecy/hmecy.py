import requests
from lxml import html
import os
from multiprocessing.dummy import Pool
import time
# https://blog.csdn.net/qq_45753992/article/details/113813352?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522166712594216782428648786%2522%252C%2522scm%2522%253A%252220140713.130102334.pc%255Fall.%2522%257D&request_id=166712594216782428648786&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~first_rank_ecpm_v1~times_rank-8-113813352-null-null.142^v62^pc_search_tree,201^v3^control_1,213^v1^t3_esquery_v1&utm_term=%E7%88%AC%E8%99%AB%E7%88%AC%E5%8F%96%E5%8D%8A%E6%AC%A1%E5%85%83&spm=1018.2226.3001.4187
#下载图片的函数，使用多线程下载
def down_img(arr):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
    }
    content = requests.get(url=arr[1][0], headers=headers).content
    with open(arr[0], 'wb')as fp:
        fp.write(content)
    print("下载完成一张")
    time.sleep(0.3)

#处理图片文件夹的标题
def correct_title(title):
    error_set = ['/', '\\', ':', '*', '?', '"', '|', '<', '>']
    for c in title:
        if c  in error_set:
            title = title.replace(c, '')
    return title

if __name__=="__main__":
    start = time.time()
    etree = html.etree

    #ajax请求的url
    # url = 'https://www.hmecy.com/wp-admin/admin-ajax.php?action=zrz_load_more_posts'
    url = 'https://www.hmecy.com/category/cos/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
    }
    #所有图片的url链接储存在这里
    all_url = []
    if not os.path.exists('./erciyuan'):
        os.mkdir('./erciyuan')

    #下载前4页的图片，可以根据自己需要更改循环次数
    for num in range(1,5):
        data = {
            'type': 'tag42',
            'paged': str(num)
        }
        #获取请求到的json函数
        response = requests.post(url=url,headers=headers,data=data).json()
        #分析json函数，发现html代码在key为msg的value中
        response = str(response['msg'])

        tree = etree.HTML(response)
        data_list = tree.xpath('//a[@class="link-block"]/@href')
        for urls in data_list:
            page_text = requests.get(url=urls,headers=headers).text
            detail_tree = etree.HTML(page_text)
            #获取标题
            title = detail_tree.xpath('//*[@id="post-single"]/h1/text()')
            #修改标题
            titles = correct_title(str(title))
            #存储的文件夹路径
            paths = './erciyuan/' + str(titles)
            url_list = detail_tree.xpath('//*[@id="content-innerText"]//img')
            data_ins = []
            i = 0
            #创建文件夹
            if not os.path.exists(paths):
                os.mkdir(paths)
            for ins in url_list:
                #获取图片的url
                data_url = ins.xpath('./@src')
                #图片的存储路径
                path = paths +'/'+ str(i) +'.jpg'
                i=i+1
                #将路径与图片的url存储到all_url中，方便后面使用多线程下载
                all_url.append([path,data_url])
    #创建4个线程
    pool = Pool(4)
    #将函数与all_url列表放入线程
    pool.map(down_img,all_url)
    print(time.time()-start)

