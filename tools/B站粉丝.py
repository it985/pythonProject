import time
from pathlib import Path
from typing import List, Dict

import requests


def get_up_fans(uid: str) -> int:
    # B站用户信息API
    url = f'https://api.bilibili.com/x/relation/stat?vmid={uid}'

    # 设置请求头，模拟浏览器访问
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        # 发送GET请求
        response = requests.get(url, headers=headers)
        data = response.json()

        # 检查请求是否成功
        if data['code'] == 0:
            follower = data['data']['follower']
            print(f'UP主(UID: {uid})的粉丝数为: {follower}')
            return follower
        else:
            print(f'获取数据失败，错误代码：{data["code"]}')
            return None

    except Exception as e:
        print(f'发生错误: {str(e)}')
        return None


def batch_get_fans(uid_list: List[str]) -> Dict[str, int]:
    """批量获取多个UP主的粉丝数"""
    results = {}
    total = len(uid_list)

    print(f"\n开始获取{total}个UP主的粉丝数据...")
    for i, uid in enumerate(uid_list, 1):
        fans_count = get_up_fans(uid)
        if fans_count is not None:
            results[uid] = fans_count
        print(f"进度: {i}/{total}")
        # 添加延时，避免请求过于频繁
        time.sleep(1)
    return results


def read_uids_from_file(filename: str) -> List[str]:
    """从文件中读取UID列表"""
    try:
        with open(filename, 'r') as f:
            # 去除空行和空格，并过滤掉无效行
            uids = [line.strip() for line in f.readlines()]
            return [uid for uid in uids if uid]
    except Exception as e:
        print(f'读取文件失败: {str(e)}')
        return []


def save_to_file_by_range(results: Dict[str, int]) -> None:
    """根据粉丝数范围将结果保存到不同文件"""
    # 创建分类字典
    ranges = {
        '20w.txt': (0, 200000),
        '40w.txt': (200000, 400000),
        '60w.txt': (400000, 600000),
        '80w.txt': (600000, 800000),
        '100w.txt': (800000, float('inf'))
    }

    # 创建结果目录
    result_dir = Path('results')
    result_dir.mkdir(exist_ok=True)

    # 初始化文件
    for filename in ranges.keys():
        file_path = result_dir / filename
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f"# 粉丝数统计 - {filename}\n")
            f.write("UID,粉丝数\n")

    # 分类写入文件
    for uid, fans in results.items():
        for filename, (min_fans, max_fans) in ranges.items():
            if min_fans <= fans < max_fans:
                file_path = result_dir / filename
                with open(file_path, 'a', encoding='utf-8') as f:
                    f.write(f"{uid},{fans}\n")
                break


if __name__ == '__main__':
    print("请选择查询方式：")
    print("1. 从文件读取UID列表")
    print("2. 手动输入多个UID")

    choice = input("请输入选择（1或2）: ")

    if choice == '1':
        filename = input("请输入UID列表文件名（例如：uids.txt）: ")
        uid_list = read_uids_from_file(filename)
    else:
        uid_input = input("请输入UID列表，用逗号分隔（例如：123,456,789）: ")
        uid_list = [uid.strip() for uid in uid_input.split(',')]

    if uid_list:
        results = batch_get_fans(uid_list)

        print("\n查询结果汇总：")
        for uid, fans in results.items():
            print(f"UID: {uid} - 粉丝数: {fans}")

        # 保存分类结果
        save_to_file_by_range(results)
        print("\n结果已保存到results目录下的相应文件中")
    else:
        print("没有有效的UID输入！")