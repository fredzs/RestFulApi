"""日志工厂类"""
import os
import logging
from logging.config import fileConfig
from config import Config
# from app.api.Service.ConfigService import ConfigService
# from app import CONFIG


class LogFactory(object):
    def __init__(self):
        try:
            # log_config_file_name = Config.get_config("Log", "log_config")
            log_config_file_name = "logging_config.ini"
            fileConfig(log_config_file_name)
        except Exception as e:
            # TODO: 默认的logger
            pass
        finally:
            self._logger = logging.getLogger()

    def get_logger(self):
        return self._logger
