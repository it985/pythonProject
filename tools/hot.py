import os
from pathlib import Path
from datetime import datetime, timedelta
import time  # 新增：用于记录运行时间


def process_markdown_file(file_path):
    global file_count  # 新增：使用全局变量来统计文件数量

    # 从文件名中提取 date 部分（格式：yyyy-mm-dd）
    file_name = file_path.name
    if file_name.endswith('.md'):
        date_str = file_name[:-3]  # 去掉 .md 后缀

        try:
            # 将字符串转为 datetime 对象
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            # 加一天
            new_date = date_obj + timedelta(days=1)
            new_date_str = new_date.strftime("%Y-%m-%d")  # 转回 yyyy-mm-dd 格式

            # 创建新的头部内容
            new_header = f"""---
title: GitHub trending {date_str} 
date: {new_date_str} 00:00:00
math: true
description: GitHub trending {date_str} 
image:
slug: {date_str} 
math: true
license: # 文章尾部显示的协议，false 为隐藏，其他作为内容，留空就是使用 config.yaml 里默认的
hidden: false # 是否隐藏，一般用不到
comments: true # 因为 bug 所以这个属性只要存在，不管是 true 还是 false 都会导致回复无法显示，需要删掉
categories:
    - GitHub
tags:
    - hot
    - 每日
    - trending
    - 热门
---

> master，这是我的[小站](https://blog.study996.cn) https://blog.study996.cn ,欢迎访问哦~~

# {date_str} - GitHub 热榜  
"""

            # 读取原文件内容
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 将新头部和原有内容组合
            new_content = new_header + '\n' + content

            # 写回文件
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)

            print(f"已处理文件: {file_path}")
            file_count += 1  # 新增：每处理一个文件，计数器加一

        except ValueError:
            print(f"错误：无法解析日期 {date_str} 在文件 {file_path}")


# 遍历指定目录中的所有 .md 文件，包括子目录
root_dir = os.path.abspath(input("请输入要处理的根目录路径："))
start_time = time.time()  # 新增：记录程序开始时间

file_count = 0  # 新增：初始化文件计数器

for dirpath, dirnames, filenames in os.walk(root_dir):
    for filename in filenames:
        if filename.endswith('.md'):
            file_path = Path(os.path.join(dirpath, filename))
            process_markdown_file(file_path)

end_time = time.time()  # 新增：记录程序结束时间
total_time = end_time - start_time  # 新增：计算总运行时间（秒）

print(f"\n所有文件处理完成！")
print(f"总共处理了 {file_count} 个文件。")
print(f"程序运行时间为：{int(total_time * 1000)} 毫秒。")  # 将秒转换为毫秒