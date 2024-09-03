import asyncio
import json
import time
import os
import tracemalloc
import aiofiles
import aiohttp
import requests

headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Connection": "keep-alive",
    "Cookie": "UM_distinctid=185f824272f16ea-0c03819193835a-7d5d547c-144000-185f824273013d6; _MHYUUID=0ad7ae5a-10e3-4505-90ce-a7c2f8f99a69; DEVICEFP_SEED_ID=60e22a286331cb28; DEVICEFP_SEED_TIME=1674905397591; _ga=GA1.1.506614920.1674905398; cookie_token_v2=v2_KNsI17S_X0gYUbQATXiScQMUXIyQnh21Xkli9VOb7T69MlsV7pY9pmHcue9A8Nf-4AuSOgMJtdBAeCV_H8JMifEjTHJ4rgjL7GeDR-Vf6w8vf6ZgL6xw; account_mid_v2=04o5cus5ih_mhy; account_id_v2=190808768; ltoken_v2=v2_OZmZlF8TYm-zlRJHSLXPSpTyHUdcYu9Os1AeUAzKomAO8in1pG9Wr2xUhzoWxgJyOqfQxuxLYRTHeIV5CADTfcRnsfqmnZzd; ltmid_v2=04o5cus5ih_mhy; ltuid_v2=190808768; DEVICEFP=38d7ee5e7377f; acw_tc=1a0c398a16834610197163803e12015234d49b965b206666b024a9a55a6a34; _ga_KS4J8TXSHQ=GS1.1.1683461019.30.1.1683461241.0.0.0",
    "DS": "1683461241,XhanrS,1457893deb5f1d6f1030fc14a6164882",
    "Host": "bbs-api.miyoushe.com",
    "Origin": "https://www.miyoushe.com",
    "Referer": "https://www.miyoushe.com/",
    "sec-ch-ua": "\"Chromium\";v=\"112\", \"Microsoft Edge\";v=\"112\", \"Not:A-Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.68",
    "x-rpc-app_version": "2.49.1",
    "x-rpc-client_type": "4",
    "x-rpc-device_id": "14403490bad4a8541bb3e466cb9929c1"
}


async def creat_path(name, use:int):
    pname = name.replace("\n", "")
    # 创建文件夹,返回路径
    path = r"./" + str(use)
    # 判断是否存在文件夹
    if not os.path.exists(path):
        os.makedirs(path)
    folder_path = os.path.join(path, pname)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    return folder_path


async def get_info(data: json):
    info_list: list = data['data']['list']
    for index, info in enumerate(info_list):
        my_dict.setdefault(info["post"]["subject"], []).extend([i for i in info["post"]["images"]])


def get_url():
    # 构造所有的链接
    my_list: list = []
    offset: int = 0
    url_offset: str = ""
    # url = "https://bbs-api.miyoushe.com/post/wapi/userPost?size=20&uid=325016524"
    url = f"https://bbs-api.miyoushe.com/post/wapi/userPost?size=20&uid={useid}"
    url_back: str = url
    while True:
        try:
            response = requests.get(url=url_offset if offset > 0 else url_back, headers=headers)
            offset = int(response.json()['data']['next_offset']) if int(
                response.json()['data']['next_offset']) != 0 else -1
            if offset != -1:
                # url_offset = f"https://bbs-api.miyoushe.com/post/wapi/userPost?offset={offset}&size=20&uid=325016524-1"
                url_offset = f"https://bbs-api.miyoushe.com/post/wapi/userPost?offset={offset}&size=20&uid={useid}"
                my_list.append(url_offset)
            url_back = ""
        except:
            my_list.insert(0, url)
            my_list.pop()
            break
    return my_list


async def creat_all(urls):
    # 创建所有任务
    tasks: list = []
    if type(urls) == list:
        for url in urls:
            task = asyncio.ensure_future(creat(urls=url))
            tasks.append(task)
        results_s = await asyncio.gather(*tasks)
        return results_s
    elif type(urls) == dict:
        listlen: int = 0
        for _key, _value in urls.items():
            listlen = len(_value) + listlen
            task = asyncio.ensure_future(creat(urls=_value, wjjname=_key))
            tasks.append(task)
        results_s = await asyncio.gather(*tasks)
        my_dict_info["foldernum"] = len(urls)
        my_dict_info["imgnum"] = listlen
        return results_s


async def creat(urls: any, wjjname=""):
    # 解析网络数据
    #下载图片时加入haders会报错
    identifier:int = 0
    async with aiohttp.ClientSession() as session:
        if isinstance(urls, str):
            urls = [urls]
        else:
            identifier = 1
            if len(urls) == 0:
                # 列表为空
                return 0
        i: int = 0
        path = await creat_path(wjjname, use=useid)
        for url in urls:
            async with session.get(url=url, headers=headers if identifier == 0 else None) as response:
                if wjjname == "":
                    conter = await response.content.read()
                    data: json = json.loads(conter)
                    await get_info(data)
                    print("处理成功...")
                    return 0
                else:
                    i = i + 1
                    await download_image(response)
                    _path = path + "\\" + str(i) + ".jpg"
                    async with aiofiles.open(_path, "wb") as f:
                        data = await response.read()
                        await f.write(data)
                        print("下载成功...")
        return 0


async def download_image(response):
    # 发送HTTP GET请求获取图片数据
    # 获取图片大小（以字节为单位）
    # print(type(response.content))
    data = await response.read()
    image_size = len(data)
    # 获取下载速度（以比特/秒为单位）
    download_speed = 10 * 1024 * 1024  # 假设下载速度为10Mbps
    # 计算下载所需时间（以秒为单位）
    download_time = image_size / download_speed
    # 计算下载所需的数据量（以MB为单位）
    download_size_mb = image_size / (1024 * 1024)
    # 返回结果
    my_load_info[download_size_mb] = download_time
    return int(download_size_mb), int(download_time)


def main():
    try:
        results = asyncio.run(creat_all(my_url_list))
    except Exception as e:
        print(f"Error occurred during execution of creat_all(my_url_list): {e}")
        results = []

    if results:
        try:
            print("<<开始下载>>")
            load_mb: int = 0
            load_time: int = 0
            results_end = asyncio.run(creat_all(my_dict))
            # print(f"<<下载完成>>")
            for key, value in my_load_info.items():
                load_mb = key + load_mb
                load_time = value + load_time
            end_time = time.time()
            elapsed_time = int(end_time - start_time)
            print(f""
                  f"程序执行时间为 {elapsed_time} 秒,"
                  f"创建了{my_dict_info['foldernum']}个文件夹,"
                  f"下载了{my_dict_info['imgnum']}个文件,"
                  f"下载耗时{int(load_time)}秒,消耗流量{int(load_mb)}mb."
                  )
        except Exception as e:
            print(f"Error occurred during execution of creat_all(my_dict): {e}")
            results_end = []
    else:
        results_end = []

    return f"results = {results}\n results_end = {results_end}"

if __name__ == '__main__':
    tracemalloc.start()
    start_time = time.time()  # 程序开始时间
    useid = input("请输入用户ID：")  # 用户ID
    try:
        useid = int(useid)
    except ValueError:
        print("无效的用户ID")
        exit()
    my_url_list: list = get_url()  # 构建出所有可以访问的帖子链接
    my_dict: dict = {}  # json数据中的标题:链接
    my_dict_info: dict = {}  # 帖子数量:链接数量
    my_load_info: dict = {}  # 下载大小:下载时间
    classify: bool = True
    main()