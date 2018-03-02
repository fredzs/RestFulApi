"""数据库测试文件"""


from app.api.Service.EmailService import EmailService
from app.api.Factory.LogFactory import LogFactory

logger = LogFactory().get_logger()


if __name__ == "__main__":
    logger.info('-----------------------------------程序开始执行-----------------------------------')
    service = EmailService()
    service.read_config()
    # check_result = service.read_config()
    check_result = service.make_statistics("2018-03-01", "2018-03-01")
    logger.info('-----------------------------------程序执行结束-----------------------------------')
