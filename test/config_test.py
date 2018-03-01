"""数据库测试文件"""

import os
import configparser
from app.api.Factory.LogFactory import LogFactory
from Config import Config
logging = LogFactory().get_logger()


def get_config(section, key):
    cfg = configparser.ConfigParser()
    path = os.path.join(os.path.split(os.path.realpath(__file__))[0] + 'config.ini')
    try:
        cfg.read(path)
    except Exception as e:
        logging.error("读取配置文件错误！")
        return ""
    return cfg.get(section, key)


if __name__ == "__main__":
    logging.info('-----------------------------------程序开始执行-----------------------------------')
    admin_password = Config.get_config("Admin", "admin_password")
    logging.info(admin_password)
    logging.info('-----------------------------------程序执行结束-----------------------------------')
