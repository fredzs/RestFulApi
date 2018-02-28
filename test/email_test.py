"""数据库测试文件"""


from app.api.Service.EmailService import EmailService
from app.api.Factory.LogFactory import LogFactory

logger = LogFactory().get_logger()


if __name__ == "__main__":
    logger.info('-----------------------------------程序开始执行-----------------------------------')
    service = EmailService()
    check_result = service.send_daily_email("2018-02-28")
    logger.info('-----------------------------------程序执行结束-----------------------------------')
