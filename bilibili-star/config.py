import os

# API配置
API_CONFIG = {
    'retry_times': 3,      # 重试次数
    'timeout': 30,         # 请求超时时间
    'min_delay': 10,        # 最小延迟(秒)
    'max_delay': 50,        # 最大延迟(秒)
    'batch_size': 10,       # 每批处理的用户数
    'batch_delay': 30,     # 批次之间的延迟(秒)
}

# 文件路径配置
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')

# 粉丝数范围配置
FANS_RANGES = {
    '10w': (0, 100000),
    '30w': (100000, 300000),
    '60w': (300000, 600000),
    '90w': (600000, 900000),
    '100w': (900000, float('inf'))
}

# 文件映射
FILE_MAPPING = {
    '10w': os.path.join(DATA_DIR, '10w.txt'),
    '30w': os.path.join(DATA_DIR, '30w.txt'),
    '60w': os.path.join(DATA_DIR, '60w.txt'),
    '90w': os.path.join(DATA_DIR, '90w.txt'),
    '100w': os.path.join(DATA_DIR, '100w.txt')
}

# 日志配置
LOG_CONFIG = {
    'log_file': os.path.join(BASE_DIR, 'crawler.log'),
    'log_level': 'INFO'
} 