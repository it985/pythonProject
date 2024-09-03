import 重命名
import logging
import threading
from datetime import datetime
from logging.handlers import RotatingFileHandler

# 定义一个函数来生成包含时间戳的日志文件名
def get_log_filename(prefix, extension):
    current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    return f'{prefix}_{current_time}{extension}'

# 获取当前时间，并格式化为字符串
current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

# 设置日志记录器，同时输出到文件和控制台
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# 使用 RotatingFileHandler 来设置日志文件分割
info_log_file = get_log_filename('a-info', '.log')
error_log_file = get_log_filename('a-error', '.log')

info_file_handler = RotatingFileHandler(info_log_file, maxBytes=5*1024*1024, backupCount=0, encoding='utf-8')
info_file_handler.setLevel(logging.INFO)
info_file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

error_file_handler = RotatingFileHandler(error_log_file, maxBytes=200*1024, backupCount=0, encoding='utf-8')
error_file_handler.setLevel(logging.ERROR)
error_file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

logger.addHandler(info_file_handler)
logger.addHandler(error_file_handler)
logger.addHandler(console_handler)

def rename_folders(directory_path):
    # 打印当前目录路径
    logger.info(f'Processing directory: {directory_path}')
    for item in os.listdir(directory_path):
        item_path = os.path.join(directory_path, item)
        if os.path.isdir(item_path):
            if item in ['图文作品', '视频作品']:
                logger.info(f'Skip renaming "{item}" as it is a special directory')
                rename_folders(item_path)
                continue
            new_name = ''.join(filter(str.isdigit, item))
            if new_name:  # 确保新名称不为空
                new_item_path = os.path.join(directory_path, new_name)
                try:
                    os.rename(item_path, new_item_path)
                    logger.info(f'Renamed "{item}" to "{new_name}"')
                except Exception as e:
                    logger.error(f'Failed to rename "{item}" to "{new_name}". Error: {type(e).__name__}: {e}')
            else:
                logger.info(f'No digits found in "{item}", skipping rename.')
            # 注意：递归调用前应该检查新路径是否存在
            if os.path.isdir(new_item_path):
                rename_folders(new_item_path)

def process_directory(directory_path):
    if os.path.isdir(directory_path):
        rename_folders(directory_path)
    else:
        logger.error(f'The provided path "{directory_path}" does not exist.')

if __name__ == '__main__':
    with open('b.txt', 'r', encoding='utf-8') as file:
        threads = []
        for line in file:
            directory_path = line.rstrip()
            thread = threading.Thread(target=process_directory, args=(directory_path,))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()
