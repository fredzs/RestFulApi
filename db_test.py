"""数据库测试文件"""


import logging
from logging.config import fileConfig
from datetime import datetime

from Entity.Performance import Performance
from Service.DBDailyService import DBDailyService

fileConfig('logging_config.ini')
LOGGER = logging.getLogger()


if __name__ == "__main__":
    LOGGER.info('-------------------------------------------'
                '程序开始执行-------------------------------------------')
    DB = DBDailyService()
    DATE = datetime.strptime("2018-01-02", "%Y-%m-%d")
    PERFORMANCE = Performance("香河园", DATE, 200, 'q', 'w', 'e', 'r')
    DB.db_save(PERFORMANCE)
    DB.db_commit()
    LOGGER.info('-------------------------------------------'
                '程序执行结束-------------------------------------------')
