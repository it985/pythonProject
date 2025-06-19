import os

import requests  # 第三方模块

# 伪装
headers = {
    'cookie': 'tt_webid=7080861394355144200; MONITOR_WEB_ID=c27b9f4a-4917-4256-be93-e948308467e3; _ga=GA1.2.129525347.1648641528; mobile_set=no; _gid=GA1.2.65241243.1648881025; ttcid=7fe011fccdef4bb499adfaa2a66fe91523; Hm_lvt_330d168f9714e3aa16c5661e62c00232=1648641528,1648881024,1648881406; s_v_web_id=verify_l1hhezfz_DPGGYf9t_xlZo_4XMT_A2sB_XTxuLFCn9F0N; _csrf_token=286c9c233158922e343eb557dff2edb6; Hm_lpvt_330d168f9714e3aa16c5661e62c00232=1648881639; _gat_gtag_UA_121535331_1=1; msToken=y0CPmCLvPhDlOHFTJ6Pbe7I6Yn_qHXWZCV6H2jCS6CSFDeOr9D2ay5oXSBenhEVJE13LumKz8r_Z_NkDf-q6YvymJb2WtmgoEhlNX-ECCMR2-cqikWcaBI2GoYLPrpQ=; tt_scid=PKf8Ei-xP9zbLe9A2gRCWsQrM.BLxDRwCzU5RwxC2Cll0u0kK09ctPib3QLfmh5i1436',
    # 'referer': 'https://bcy.net/coser/toppost100?type=week&date=20220319',
    'referer': 'https://bcy.net/coser/toppost100?type=week',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36'
}
url = 'https://bcy.net/apiv3/rank/list/itemInfo'
params = {
    # 'p': '1',
    'ttype': 'cos',
    'sub_type': 'week',
    # 'date': '20220319'
}
# 1. 发送请求
response = requests.get(url=url, headers=headers, params=params)
# 2. 获取数据
json_data = response.json()
# 3. 解析数据
# 结构化数据   json数据       字典键值对取值 re
# 非结构化数据 html网页 网页源代码 css xpath re
top_list = json_data['data']['top_list_item_info']
for top in top_list:
    uname = top['item_detail']['uname']
    print(f'正在爬取: {uname}')
    if not os.path.exists(f'img/{uname}'):
        os.mkdir(f'img/{uname}')
    image_list = top['item_detail']['image_list']
    for img in image_list:
        path = img['path']
        mid = str(img['mid'])
        print(f'    {mid}.jpg')
        # 4. 保存数据
        img_data = requests.get(path).content
        with open(f'img/{uname}/{mid}.jpg', mode='wb') as f:
            f.write(img_data)
