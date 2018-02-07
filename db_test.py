"""数据库测试文件"""


from datetime import datetime
import logging
from logging.config import fileConfig
from Service.PerformanceService import PerformanceService

fileConfig('logging_config.ini')
LOGGER = logging.getLogger()

p = {
        'dept_id': 2,
        'date': '2018-02-07',
        "submit_user": "fred",
        "extra_fields": {
            "field_1": {
                "field_id": "1",
                "filed_value": 300
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
    }

if __name__ == "__main__":
    LOGGER.info('-----------------------------------'
                '程序开始执行-----------------------------------')
    SERVICE = PerformanceService()
    PERFORMANCE = PerformanceService.read_json(p)
    SERVICE.submit_performance(PERFORMANCE)
    date = datetime.strptime("2018-02-07", "%Y-%m-%d")
    check_result = PerformanceService.check_submission(date)
    LOGGER.info(check_result)
    LOGGER.info('-----------------------------------'
                '程序执行结束-----------------------------------')
