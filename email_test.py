"""数据库测试文件"""


from app.api.Service.EmailService import EmailService
from app.api.Factory.LogFactory import LogFactory
from Config import GLOBAL_CONFIG
logger = LogFactory().get_logger()


if __name__ == "__main__":
    logger.info('-----------------------------------程序开始执行-----------------------------------')
    service = EmailService()
    service.read_config()
    check_result = service.send_range_email("2018-03-01", "2018-03-12")
    logger.info('-----------------------------------程序执行结束-----------------------------------')
