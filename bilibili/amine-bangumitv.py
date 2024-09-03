import requests
import os
import json
def fetch_and_save_urls(url, base_output_dir):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    page = 1
    while True:
        # 构建带有当前页码的 URL
        url_with_page = f"{url}&page={page}"
        print("当前 URL:", url_with_page)  # 输出当前 URL

        response = requests.get(url_with_page, headers=headers)

        # 检查状态码
        if response.status_code != 200:
            print("状态码不是200，停止循环。")
            break

        # 解析响应内容，这里假设响应内容是JSON格式
        data = response.json()

        # 假设JSON数据中有一个名为urls的键，包含了URL列表
        urls = data.get('urls', [])

        # 获取当前工作目录的路径
        current_directory = os.getcwd()

        # 构建输出目录
        output_dir = os.path.join(current_directory, base_output_dir)

        # 确保输出目录存在
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # 构建当前页码的JSON文件名
        output_file_name = f"page_{page}.json"
        output_file_path = os.path.join(output_dir, output_file_name)

        # 将当前页码的URL列表保存到JSON文件中
        with open(output_file_path, 'w', encoding='utf-8') as file:
            json.dump(urls, file, ensure_ascii=False, indent=4)

        # 更新页码
        page += 1

# 调用函数
fetch_and_save_urls(
    "https://api.bilibili.com/pgc/season/index/result?st=1&order=3&season_version=-1&spoken_language_type=-1&area=-1&is_finish=-1&copyright=-1&season_status=-1&season_month=-1&style_id=-1&sort=0&season_type=1&pagesize=20&type=1",
    "bilibili_urls")
