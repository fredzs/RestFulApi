"""数据库测试文件"""


import logging
from logging.config import fileConfig
from datetime import datetime

from Entity.Performance import Performance
from Service.DBDailyService import DBDailyService

fileConfig('logging_config.ini')
LOGGER = logging.getLogger()

p = [
    {
        'dept_name': 1,
        'date': '2018-01-01',
        'submit_date': '2018-02-06',
        "submit_user": "fred",
        'project_1': 100,
        "extra_fields": {
            "field_1": {
                "field_id": "1",
                "filed_value": 100
            },
            "field_2": {
                "field_id": "2",
                "filed_value": 10
            },
            "field_3": {
                "field_id": "3",
                "filed_value": 10
            },
            "field_4": {
                "field_id": "4",
                "filed_value": "10"
            }
        }
    },
    {
        'dept_name': 1,
        'date': '2018-02-01',
        "submit_user": "fred",
        'project_1': 200
    }]

if __name__ == "__main__":
    LOGGER.info('-----------------------------------'
                '程序开始执行-----------------------------------')
    DB = DBDailyService()
    DATE = datetime.strptime("2018-02-02", "%Y-%m-%d")
    PERFORMANCE = Performance("首都机场", DATE, "顾铮", 300)
    DB.db_save(PERFORMANCE)
    DB.db_commit()
    LOGGER.info('-----------------------------------'
                '程序执行结束-----------------------------------')
