"""日志工厂类"""
import os
import logging
from logging.config import fileConfig

from app.api.Entity.Config import Config


class ConfigFactory(object):
    config = Config()

    @classmethod
    def read_config(cls, config_file_name):
        with open(config_file_name, 'r') as f:
            for line in f:
                line = line.strip('\n')
                key = line[:line.index(' = ')]
                value = line[line.index(' = ') + 3:]
                cls.config.add_config_field(key, value)
        return cls.config
