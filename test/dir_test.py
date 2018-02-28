"""数据库测试文件"""

import sys, os
from app.api.Factory.LogFactory import LogFactory

#import logging
from app.api.Factory.ConfigFactory import ConfigFactory
from app import CONFIG
logging = LogFactory().get_logger()
# logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')


if __name__ == "__main__":
    logging.info('-----------------------------------程序开始执行-----------------------------------')
    log_dir = os.path.join(os.getcwd(), "logging_config.ini").replace("\\","/")
    logging.info(log_dir)
    dir1 = os.path.abspath('.')
    logging.info(dir1)
    base_dir = os.path.dirname(__file__)
    logging.info(base_dir)
    logging.info(CONFIG.get_config_field("admin_password"))
    logging.info('-----------------------------------程序执行结束-----------------------------------')
