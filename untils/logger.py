import logging
import os
from pathlib import Path
import datetime
from logging.handlers import RotatingFileHandler
import colorlog
from config.settings import BASE_DIR

# 安全地处理路径
LOG_DIR = Path(BASE_DIR) / 'logs'
try:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
except Exception as e:
    print(f"Failed to create log directory: {e}")
    exit(1)

logger = logging.getLogger("api_test")
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# 使用 UTC 时间戳确保唯一性
log_file = LOG_DIR / f"{datetime.datetime.utcnow().strftime('%Y-%m-%d')}.log"
try:
    file_handler = RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=5, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
except Exception as e:
    print(f"Failed to create file handler: {e}")
    exit(1)

# 使用 colorlog.ColoredFormatter
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
colored_formatter = colorlog.ColoredFormatter(
    '%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
    }
)
console_handler.setFormatter(colored_formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

if __name__ == '__main__':
    logger.debug('This is a debug message.')
    logger.info('This is an info message.')
    logger.warning('This is a warning message.')
    logger.error('This is an error message.')
    logger.critical('This is a critical message.')