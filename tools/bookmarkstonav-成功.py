import json
import yaml
import 重命名
from urllib.parse import urlparse, urlunparse


def extract_taxonomy(path):
    # 提取路径中 ${BOOKMARKS_BAR} 后面的路径，并返回切割后的路径部分
    return path.split('${BOOKMARKS_BAR}/')[-1]


def convert_json_to_yaml(json_data):
    dict_data = []
    taxonomies = {}
    seen_urls = set()  # 用于跟踪已处理的 URL

    for bookmark in json_data["bookmarks"]:
        title = bookmark["title"]
        url = bookmark["url"]
        path_segments = extract_taxonomy(bookmark["path"]).split('/')
        taxonomy = path_segments[0] if path_segments else "未分类"
        term = path_segments[1] if len(path_segments) > 1 else None

        # 使用 urlparse 提取 hostname，去掉 http:// 和 https:// 前缀
        parsed_url = urlparse(url)
        hostname = parsed_url.hostname

        # 如果 hostname 为空，则认为是无效的 URL
        if hostname is None:
            print(f"无效的 URL: {url}, 对应的路径: {bookmark['path']},对应的标题:{bookmark['title']}")
            continue

        # 去掉 http:// 和 https:// 前缀
        if hostname.startswith('www.'):
            hostname = hostname[4:]

        # 构建新的 URL 结构
        new_url = urlunparse((parsed_url.scheme, hostname, '/'.join(parsed_url.path.split('/')[-4:]), '', '', ''))

        # 如果该 URL 已经处理过，则跳过
        if new_url in seen_urls:
            continue
        seen_urls.add(new_url)  # 将新处理的 URL 添加到集合中

        # 设置默认的 favicon URL
        favicon_local_path = f"https://api.iowen.cn/favicon/{hostname}.png"

        # 使用默认的 favicon URL
        if taxonomy not in taxonomies:
            taxonomies[taxonomy] = {
                "taxonomy": taxonomy,
                "icon": "far fa-star"  # 设置统一的分类图标
            }

        link_dict = {
            "title": title,
            "logo": favicon_local_path,  # 使用默认的 favicon URL
            "url": new_url,  # 使用新的 URL 结构
            "description": ""
        }

        # 将链接字典添加到对应的 taxonomy 中
        if taxonomy in taxonomies:
            if "links" not in taxonomies[taxonomy]:
                taxonomies[taxonomy]["links"] = []
            taxonomies[taxonomy]["links"].append(link_dict)

    # 将 taxonomies 转换为列表
    for taxonomy_info in taxonomies.values():
        dict_data.append(taxonomy_info)

    return dict_data


# 从 Json Bookmarks 导出的文件 bookmarks.v2.json 提取 json 数据
json_file_path = 'bookmarks.v2.json'
with open(json_file_path, 'r', encoding='utf-8') as file:
    json_data = json.load(file)

# 将字典转换为 YAML 格式
yaml_data = convert_json_to_yaml(json_data)
yaml_output = yaml.dump(yaml_data, default_flow_style=False, allow_unicode=True, sort_keys=False)

# 将 YAML 数据写入到文件 webstack.yml
with open('webstack.yml', 'w', encoding='utf-8') as file:
    file.write(yaml_output)

print('YAML data has been written to webstack.yml')
