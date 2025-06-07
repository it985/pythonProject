import asyncio
import aiohttp
import logging
import sys
from typing import List, Dict, Any
from config import API_CONFIG
from utils import random_delay, get_fans_range, save_to_file, ensure_data_dir, log_error


# 配置日志
def setup_logging():
    # 创建日志记录器
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # 创建日志格式
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # 创建文件处理器
    file_handler = logging.FileHandler('crawler.log', encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    # 创建控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # 添加处理器到记录器
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


class BilibiliFansCrawler:
    def __init__(self):
        self.session = None
        self.processed_count = 0
        self.failed_count = 0
        self.fans_stats = {
            '10w': 0,
            '30w': 0,
            '60w': 0,
            '90w': 0,
            '100w': 0
        }
        logging.info("爬虫初始化完成")

    async def init_session(self):
        """初始化会话"""
        try:
            if not self.session:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                    'Referer': 'https://www.bilibili.com',
                    'Origin': 'https://www.bilibili.com',
                    'Accept': 'application/json, text/plain, */*',
                    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Connection': 'keep-alive'
                }
                self.session = aiohttp.ClientSession(headers=headers)
                logging.info("会话初始化完成")
        except Exception as e:
            log_error("初始化会话失败", e)
            raise

    async def close_session(self):
        """关闭会话"""
        try:
            if self.session:
                await self.session.close()
                self.session = None
                logging.info("会话已关闭")
        except Exception as e:
            log_error("关闭会话失败", e)

    async def get_user_info(self, uid: int) -> Dict[str, Any]:
        """获取用户信息"""
        logging.info(f"开始获取用户 {uid} 的信息")
        for i in range(API_CONFIG['retry_times']):
            try:
                url = f"https://api.bilibili.com/x/web-interface/card?mid={uid}"
                async with self.session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        print(f"API响应: {data}")

                        if data['code'] == 0 and 'data' in data:
                            user_data = data['data']
                            print(f"用户数据: {user_data}")

                            # 从data中获取粉丝数
                            if 'follower' in user_data:
                                print(f"获取到粉丝数: {user_data['follower']}")
                                return user_data
                            else:
                                print("警告: 未找到粉丝数信息")
                                print(f"用户数据字段: {list(user_data.keys()) if user_data else 'None'}")
                        else:
                            print(f"API返回错误: {data['message']}")
                            if data['code'] == -352:
                                print("请求被限制，等待后重试...")
                                await asyncio.sleep(API_CONFIG['min_delay'] * 2)
                    else:
                        print(f"HTTP请求失败: {response.status}")

                logging.info(f"成功获取用户 {uid} 的信息")
                return None
            except Exception as e:
                log_error(f"获取用户 {uid} 信息失败 (尝试 {i + 1}/{API_CONFIG['retry_times']})", e)
                if i < API_CONFIG['retry_times'] - 1:
                    await asyncio.sleep(API_CONFIG['min_delay'] * (i + 1))
        return None

    async def process_user(self, uid: int):
        """处理单个用户"""
        try:
            info = await self.get_user_info(uid)
            if not info:
                self.failed_count += 1
                logging.error(f"用户 {uid} 处理失败")
                return

            # 获取粉丝数
            fans_count = info.get('follower', 0)
            print(f"\n处理用户 {uid}:")
            print(f"获取到的粉丝数: {fans_count}")

            # 确保粉丝数是整数
            try:
                fans_count = int(fans_count)
            except (ValueError, TypeError):
                print(f"警告: 粉丝数转换失败，原始值: {fans_count}")
                fans_count = 0

            range_key = get_fans_range(fans_count)
            print(f"分类结果: {range_key}")

            save_to_file(uid, fans_count, range_key)
            self.fans_stats[range_key] += 1
            self.processed_count += 1

            if self.processed_count % 10 == 0:
                self.print_stats()

        except Exception as e:
            log_error(f"处理用户 {uid} 失败", e)
            self.failed_count += 1

    def print_stats(self):
        """打印统计信息"""
        print("\n当前统计信息:")
        print(f"总处理数: {self.processed_count}")
        print(f"失败数: {self.failed_count}")
        print("\n粉丝数分布:")
        print(f"10w以下: {self.fans_stats['10w']}个")
        print(f"10w-30w: {self.fans_stats['30w']}个")
        print(f"30w-60w: {self.fans_stats['60w']}个")
        print(f"60w-90w: {self.fans_stats['90w']}个")
        print(f"90w以上: {self.fans_stats['100w']}个")
        print("-" * 30)

    async def process_batch(self, uids: List[int]):
        """处理一批用户"""
        tasks = []
        for uid in uids:
            task = asyncio.create_task(self.process_user(uid))
            tasks.append(task)
            await asyncio.sleep(API_CONFIG['min_delay'])

        await asyncio.gather(*tasks)
        await asyncio.sleep(API_CONFIG['batch_delay'])

    async def process_users(self, uids: List[int]):
        """批量处理用户"""
        logging.info(f"开始处理 {len(uids)} 个用户")
        try:
            await self.init_session()
            ensure_data_dir()

            # 分批处理用户
            batch_size = API_CONFIG['batch_size']
            for i in range(0, len(uids), batch_size):
                batch = uids[i:i + batch_size]
                logging.info(f"处理第 {i // batch_size + 1} 批，共 {len(batch)} 个用户")
                await self.process_batch(batch)

            await self.close_session()
            self.print_stats()
            logging.info(f"处理完成! 成功: {self.processed_count}, 失败: {self.failed_count}")
        except Exception as e:
            log_error("批量处理用户失败", e)
            raise


async def main():
    # 使用一些不同粉丝数的UP主UID作为示例
    uids =[]
    print("开始运行爬虫...")
    crawler = BilibiliFansCrawler()
    await crawler.process_users(uids)


if __name__ == "__main__":
    print("程序启动...")
    setup_logging()  # 设置日志
    asyncio.run(main())