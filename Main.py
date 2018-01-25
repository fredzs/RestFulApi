import logging
from logging.config import fileConfig
from datetime import datetime

from Entity.Performance import Performance
from Service.DBDailyService import DBDailyService

fileConfig('logging_config.ini')
logger = logging.getLogger()


if "__main__" == __name__:
    logger.info('-------------------------------------------'
                '程序开始执行-------------------------------------------')
    db = DBDailyService()
    date = datetime.strptime("2018-01-02", "%Y-%m-%d")
    performance = Performance("香河园", date, 200, 'q', 'w', 'e', 'r')
    db.db_save(performance)
    db.db_commit()
    logger.info('-------------------------------------------'
                '程序执行结束-------------------------------------------')
