"""数据库测试文件"""

import logging
from logging.config import fileConfig
import os

dir1 = os.path.abspath("logging_config.ini").replace("\\","/")
fileConfig('../logging_config.ini')
LOGGER = logging.getLogger()


if __name__ == "__main__":
    LOGGER.info('-----------------------------------程序开始执行-----------------------------------')
    log_dir = os.path.join(os.getcwd(), "logging_config.ini").replace("\\","/")
    LOGGER.info(log_dir)
    dir1 = os.path.abspath("logging_config.ini")
    LOGGER.info(dir1)

    LOGGER.info('-----------------------------------程序执行结束-----------------------------------')
