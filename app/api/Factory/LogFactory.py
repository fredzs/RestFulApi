"""日志工厂类"""
import os
import logging
from logging.config import fileConfig
from app import CONFIG


class LogFactory(object):
    def __init__(self):
        log_config_file_name = CONFIG.get_config_field("log_config")
        if os.path.exists(log_config_file_name):
            fileConfig(log_config_file_name)
        self._logger = logging.getLogger()

    def get_logger(self):
        return self._logger
