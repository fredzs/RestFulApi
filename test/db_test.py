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
    "dept_id": 1,
    "date": "2018-03-23",
    "submit_user": "张晟",
    "extra_fields":
        {"field_1": "0", "field_2": "7", "field_3": "2", "field_4": "0", "field_5": "927", "field_6": "+927",
         "field_7": "0", "field_8": "0", "field_9": "0", "comments": "fred", "field_10": "0", "field_11": "23",
         "field_12": "470", "field_13": "0"}
}

if __name__ == "__main__":
    LOGGER.info('-----------------------------------程序开始执行-----------------------------------')
    SERVICE = PerformanceService()
    result = SERVICE.submit_performance(p2)
    # PERFORMANCE = PerformanceService.read_json(p2)
    # PERFORMANCE.rewrite_extra_fields()
    # SERVICE.submit_performance(PERFORMANCE)
    # date = datetime.strptime("2018-02-28", "%Y-%m-%d")
    # p = PerformanceService()
    # check_result = p.display(date, "支行营业室")
    # fields_info_service = FieldsInfoService()
    # fields_list = fields_info_service.find_fields_list()
    # LOGGER.info(check_result)
    LOGGER.info('-----------------------------------程序执行结束-----------------------------------')
