"""数据库测试文件"""


from datetime import datetime
import logging
from logging.config import fileConfig
from app.api.Service.FieldsInfoService import FieldsInfoService
from app.api.Service.PerformanceService import PerformanceService
from app.api.Service.DBService import DBService

fileConfig('../logging_config.ini')
LOGGER = logging.getLogger()

p2 = {
        'dept_id': 2,
        'date': '2018-02-06',
        "submit_user": "fred",
        "extra_fields":
            [{"field_id": "field_1", "field_value": 500},
            {"field_id": "field_2", "field_value": 10},
            {"field_id": "field_3", "field_value": 10},
            {"field_id": "field_4", "field_value": "10"}]
    }

if __name__ == "__main__":
    LOGGER.info('-----------------------------------程序开始执行-----------------------------------')
    SERVICE = PerformanceService()
    #PERFORMANCE = PerformanceService.read_json(p2)
    #PERFORMANCE.rewrite_extra_fields()
    #SERVICE.submit_performance(PERFORMANCE)
    date = datetime.strptime("2018-02-28", "%Y-%m-%d")
    p = PerformanceService()
    check_result = p.display(date, "支行营业室")
    #fields_info_service = FieldsInfoService()
    #fields_list = fields_info_service.find_fields_list()
    LOGGER.info(check_result)
    LOGGER.info('-----------------------------------程序执行结束-----------------------------------')
