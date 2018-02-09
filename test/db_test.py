"""数据库测试文件"""


from datetime import datetime
import logging
from logging.config import fileConfig

from app.api.Service.FieldsInfoService import FieldsInfoService
from app.api.Service.PerformanceService import PerformanceService
from app.api.Service.DBService import DBService

fileConfig('../logging_config.ini')
LOGGER = logging.getLogger()

p = {
        'dept_id': 2,
        'date': '2018-02-06',
        "submit_user": "fred",
        "extra_fields": {
            "field_1": {
                "field_id": "1",
                "filed_value": 500
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
    LOGGER.info('-----------------------------------程序开始执行-----------------------------------')
    SERVICE = PerformanceService()
    #PERFORMANCE = PerformanceService.read_json(p)
    #SERVICE.submit_performance(PERFORMANCE)
    date = datetime.strptime("2018-02-07", "%Y-%m-%d")
    p = PerformanceService()
    check_result = p.check_submission(date)
    #fields_info_service = FieldsInfoService()
    #fields_list = fields_info_service.find_fields_list()
    #LOGGER.info(fields_list)
    LOGGER.info('-----------------------------------程序执行结束-----------------------------------')
