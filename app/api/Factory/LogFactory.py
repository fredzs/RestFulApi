"""日志工厂类"""
import os
import logging
from logging.config import fileConfig


class LogFactory(object):
    def __init__(self):
        dir1 = os.path.abspath("logging_config.ini").replace("\\", "/")
        log_file_dir = os.path.join(dir1)
        fileConfig('logging_config.ini')
        self._logger = logging.getLogger()

    def get_logger(self):
        return self._logger
