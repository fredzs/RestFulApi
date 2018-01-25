import logging
from logging.config import fileConfig


fileConfig('logging_config.ini')
logger = logging.getLogger()


if "__main__" == __name__:
    logger.info('-------------------------------------------'
                '程序开始执行-------------------------------------------')
    pass
    logger.info('-------------------------------------------'
                '程序执行结束-------------------------------------------')
