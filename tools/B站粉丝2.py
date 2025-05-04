import requests
import json
import time
from typing import List, Dict, Set
from pathlib import Path
import pickle
import random

# 写一个python，分批获取UP主的粉丝数，根据粉丝数范围将结果保存到不同文件，
# 10w以内的粉丝保存到10w.txt，10w到30w的粉丝保存到30w.txt，
# 30w到60w的粉丝保存到60w.txt，60w到90w的粉丝保存到90w.txt，
# 90w以上的粉丝保存到100w.txt，
# 需要获取很多个up主的粉丝，超过1000个，所以注意风控

class FansCounter:
    def __init__(self):
        self.results = {}
        self.failed_uids = set()
        self.processed_uids = set()
        self.checkpoint_file = Path('checkpoint.pkl')
        self.max_retries = 3
        self.base_delay = 1
        self.max_delay = 3

    def load_checkpoint(self) -> None:
        """加载断点数据"""
        if self.checkpoint_file.exists():
            try:
                with open(self.checkpoint_file, 'rb') as f:
                    data = pickle.load(f)
                    self.results = data['results']
                    self.processed_uids = data['processed']
                    self.failed_uids = data['failed']
                print(f"已加载断点数据: {len(self.results)}个结果, {len(self.failed_uids)}个失败")
            except Exception as e:
                print(f"加载断点数据失败: {e}")

    def save_checkpoint(self) -> None:
        """保存断点数据"""
        try:
            with open(self.checkpoint_file, 'wb') as f:
                data = {
                    'results': self.results,
                    'processed': self.processed_uids,
                    'failed': self.failed_uids
                }
                pickle.dump(data, f)
        except Exception as e:
            print(f"保存断点数据失败: {e}")

    def get_up_fans(self, uid: str, retry_count: int = 0) -> int:
        """获取单个UP主的粉丝数，支持重试"""
        url = f'https://api.bilibili.com/x/relation/stat?vmid={uid}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        try:
            response = requests.get(url, headers=headers, timeout=10)
            data = response.json()

            if data['code'] == 0:
                follower = data['data']['follower']
                return follower
            else:
                raise Exception(f"API错误代码：{data['code']}")

        except Exception as e:
            if retry_count < self.max_retries:
                delay = min(self.base_delay * (2 ** retry_count) + random.random(), self.max_delay)
                print(f"UID {uid} 获取失败 ({e}), {delay:.1f}秒后重试 ({retry_count + 1}/{self.max_retries})")
                time.sleep(delay)
                return self.get_up_fans(uid, retry_count + 1)
            else:
                print(f"UID {uid} 最终获取失败: {e}")
                return None

    def batch_get_fans(self, uid_list: List[str], chunk_size: int = 100) -> None:
        """分批获取UP主的粉丝数"""
        # 加载之前的进度
        self.load_checkpoint()

        # 过滤掉已处理的UID
        remaining_uids = [uid for uid in uid_list if uid not in self.processed_uids]
        total = len(remaining_uids)

        if not remaining_uids:
            print("所有UID都已处理完成！")
            return

        print(f"\n开始获取{total}个UP主的粉丝数据...")

        # 分批处理
        for i in range(0, total, chunk_size):
            chunk = remaining_uids[i:i + chunk_size]
            print(f"\n处理第{i + 1}-{min(i + chunk_size, total)}个UID")

            for j, uid in enumerate(chunk, 1):
                fans_count = self.get_up_fans(uid)
                if fans_count is not None:
                    self.results[uid] = fans_count
                    self.processed_uids.add(uid)
                else:
                    self.failed_uids.add(uid)

                print(f"进度: {i + j}/{total} - UID {uid}: {fans_count if fans_count is not None else '获取失败'}")

                # 随机延时0.5-1.5秒
                time.sleep(0.5 + random.random())

            # 每个批次完成后保存断点
            self.save_checkpoint()
            print(f"已保存断点数据，当前完成：{len(self.results)}个")

            # 每个批次后额外休息2-3秒
            time.sleep(2 + random.random())


def save_to_file_by_range(results: Dict[str, int]) -> None:
    """根据粉丝数范围将结果保存到不同文件"""
    # 创建分类字典
    ranges = {
        '10w.txt': (0, 100000),
        '40w.txt': (100000, 300000),
        '60w.txt': (300000, 600000),
        '90w.txt': (600000, 900000),
        '100w.txt': (900000, float('inf'))
    }

    # 创建结果目录
    result_dir = Path('results')
    result_dir.mkdir(exist_ok=True)

    # 按范围对UID进行分类
    classified_uids = {filename: [] for filename in ranges.keys()}
    for uid, fans in results.items():
        for filename, (min_fans, max_fans) in ranges.items():
            if min_fans <= fans < max_fans:
                classified_uids[filename].append(uid)
                break

    # 保存到文件
    for filename, uids in classified_uids.items():
        if uids:  # 只保存有数据的文件
            file_path = result_dir / filename
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(','.join(uids))


def read_uids_from_file(filename: str) -> List[str]:
    """从文件中读取UID列表"""
    try:
        with open(filename, 'r') as f:
            uids = [line.strip() for line in f.readlines()]
            # 去除重复的UID
            return list(dict.fromkeys([uid for uid in uids if uid]))
    except Exception as e:
        print(f'读取文件失败: {str(e)}')
        return []


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
        counter = FansCounter()
        counter.batch_get_fans(uid_list)

        if counter.results:
            print("\n查询结果汇总：")
            print(f"成功查询：{len(counter.results)}个")
            print(f"失败数量：{len(counter.failed_uids)}个")

            if counter.failed_uids:
                print("\n失败的UID：")
                print(', '.join(counter.failed_uids))

            # 保存分类结果
            save_to_file_by_range(counter.results)
            print("\n结果已保存到results目录下的相应文件中")
    else:
        print("没有有效的UID输入！")