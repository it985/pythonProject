import asyncio
import logging
import os
import random
from typing import Optional

from config import API_CONFIG, LOG_CONFIG, FILE_MAPPING

# 配置日志
logging.basicConfig(
    level=LOG_CONFIG['log_level'],
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_CONFIG['log_file'], encoding='utf-8'),
        logging.StreamHandler()
    ]
)


async def random_delay() -> None:
    """随机延迟函数，用于避免请求过快"""
    delay = random.uniform(API_CONFIG['min_delay'], API_CONFIG['max_delay'])
    await asyncio.sleep(delay)


def get_fans_range(fans_count: int) -> str:
    """根据粉丝数获取对应的范围标识"""
    print(f"处理粉丝数: {fans_count}")  # 添加控制台输出
    logging.info(f"处理粉丝数: {fans_count}")

    # 确保fans_count是整数
    fans_count = int(fans_count)

    if fans_count >= 900000:
        print(f"粉丝数 {fans_count} 属于 100w+ 范围")
        return '100w'
    elif fans_count >= 600000:
        print(f"粉丝数 {fans_count} 属于 60w-90w 范围")
        return '90w'
    elif fans_count >= 300000:
        print(f"粉丝数 {fans_count} 属于 30w-60w 范围")
        return '60w'
    elif fans_count >= 100000:
        print(f"粉丝数 {fans_count} 属于 10w-30w 范围")
        return '30w'
    else:
        print(f"粉丝数 {fans_count} 属于 10w以下 范围")
        return '10w'


def save_to_file(uid: int, fans_count: int, range_key: str) -> None:
    """保存UP主信息到对应文件"""
    try:
        file_path = FILE_MAPPING[range_key]
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(f"{uid},{fans_count}\n")
        print(f"成功保存用户 {uid} 到 {range_key} 文件，粉丝数: {fans_count}")  # 添加控制台输出
        logging.info(f"成功保存用户 {uid} 到 {range_key} 文件，粉丝数: {fans_count}")
    except Exception as e:
        logging.error(f"保存文件失败: {str(e)}")


def ensure_data_dir() -> None:
    """确保数据目录存在"""
    for file_path in FILE_MAPPING.values():
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        if not os.path.exists(file_path):
            with open(file_path, 'w', encoding='utf-8') as f:
                pass


def log_error(message: str, error: Optional[Exception] = None) -> None:
    """记录错误日志"""
    if error:
        logging.error(f"{message}: {str(error)}")
    else:
        logging.error(message) 