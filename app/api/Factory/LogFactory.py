"""日志工厂类"""
import logging
from logging.config import fileConfig


class LogFactory(object):
    def __init__(self):
        fileConfig('logging_config.ini')
        self._logger = logging.getLogger()

    def get_logger(self):
        return self._logger
