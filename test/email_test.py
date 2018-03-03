<<<<<<< HEAD
"""数据库测试文件"""


from app.api.Service.EmailService import EmailService
from app.api.Factory.LogFactory import LogFactory

logger = LogFactory().get_logger()


if __name__ == "__main__":
    logger.info('-----------------------------------程序开始执行-----------------------------------')
    service = EmailService()
    service.read_config()
    check_result = service.read_config()
    check_result = service.send_daily_email("2018-03-01")
    logger.info('-----------------------------------程序执行结束-----------------------------------')
=======
"""数据库测试文件"""


from app.api.Service.EmailService import EmailService
from app.api.Factory.LogFactory import LogFactory

logger = LogFactory().get_logger()


if __name__ == "__main__":
    logger.info('-----------------------------------程序开始执行-----------------------------------')
    service = EmailService()
    service.read_config()
    check_result = service.send_range_email("2018-03-02", "2018-03-02")
    logger.info('-----------------------------------程序执行结束-----------------------------------')
>>>>>>> b010fb2eff0d466ec73f41c8703ee1e64d6543ac
