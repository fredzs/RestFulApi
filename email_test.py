"""数据库测试文件"""


from app.api.Service.EmailService import EmailService
from app.api.Factory.LogFactory import LogFactory
from Config import GLOBAL_CONFIG
from app.api.Service.StatisticsService import StatisticsService

logger = LogFactory().get_logger()


if __name__ == "__main__":
    logger.info('-----------------------------------程序开始执行-----------------------------------')
    service = StatisticsService()
    # check_result = service.create_files("2018-03-23", "2018-03-23", "daily")
    check_result = service.create_files("2018-03-01", "2018-03-23", "range")
    # check_result = service.create_files("2018-03-01", "2018-03-23", "detail")
    logger.info('-----------------------------------程序执行结束-----------------------------------')
