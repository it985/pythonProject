import re
# https://blog.csdn.net/weixin_44042821/article/details/121984881?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522166712596416782390586284%2522%252C%2522scm%2522%253A%252220140713.130102334.pc%255Fall.%2522%257D&request_id=166712596416782390586284&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~first_rank_ecpm_v1~times_rank-3-121984881-null-null.142^v62^pc_search_tree,201^v3^control_1,213^v1^t3_esquery_v1&utm_term=%E7%88%AC%E8%99%AB%E7%88%AC%E5%8F%96%E5%8D%8A%E6%AC%A1%E5%85%83&spm=1018.2226.3001.4187

def get_item(item_ids):
    intercepts = []
    for id in item_ids:
        url = 'https://bcy.net/item/detail/' + str(id) + '?_source_page=hashtag'
        response = requests.get(url, headers=header)
        response.encoding = 'utf-8'
        text = response.text
        intercept = text[text.index('JSON.parse("') + len('JSON.parse("'): text.index('");')].replace(r'\"', r'"')
        intercepts.append(intercept)
    return intercepts


def download(intercepts):
    for i in intercepts:
        pattern = re.compile('"multi":\[{"path":"(.*?)","type"')
        pattern_item_id = re.compile('"post_data":{"item_id":"(.*?)","uid"')
        b = pattern.findall(i)
        item_id = pattern_item_id.findall(i)[0]
        index = 0
        for url in b:
            index = index + 1
            content = re.sub(r'(\\u[a-zA-Z0-9]{4})', lambda x: x.group(1).encode("utf-8").decode("unicode-escape"), url)
            response = requests.get(content.replace('\\', ''))
            with open('D:\\bcy\\' + str(item_id) + str(index) + '.png', 'wb') as f:
                f.write(response.content)
