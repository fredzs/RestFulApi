"""数据库测试文件"""


import logging
from logging.config import fileConfig
from app.api.Service.EmailService import EmailService

fileConfig('../logging_config.ini')
LOGGER = logging.getLogger()


if __name__ == "__main__":
    LOGGER.info('-----------------------------------程序开始执行-----------------------------------')
    SERVICE = EmailService()
    check_result = SERVICE.send_email("2018-02-23")
    LOGGER.info('-----------------------------------程序执行结束-----------------------------------')
