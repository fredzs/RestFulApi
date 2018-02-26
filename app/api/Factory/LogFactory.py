"""日志工厂类"""
import os
import logging
from logging.config import fileConfig

fileConfig('logging_config.ini')
logger = logging.getLogger()


class LogFactory(object):
    def __init__(self):
        dir1 = os.path.abspath("logging_config.ini").replace("\\", "/")
        log_file_dir = os.path.join(dir1)

    # def get_logger(self):
    #     return self._logger
