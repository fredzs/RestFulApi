"""数据库测试文件"""

import os
from app.api.Factory.LogFactory import LogFactory

logger = LogFactory().get_logger()


if __name__ == "__main__":
    logger.info('-----------------------------------程序开始执行-----------------------------------')
    log_dir = os.path.join(os.getcwd(), "logging_config.ini").replace("\\","/")
    logger.info(log_dir)
    dir1 = os.path.abspath("logging_config.ini")
    logger.info(dir1)
    base_dir = os.path.dirname(__file__)
    logger.info(os.path.join(base_dir, "logging_config.ini"))

    logger.info('-----------------------------------程序执行结束-----------------------------------')
