import os
import configparser


class Config(object):
    def __init__(self):
        self._path = os.path.join(os.path.split(os.path.realpath(__file__))[0] + '/config.ini')
        self._config = configparser.ConfigParser()
        self.read_config_file(self._path)

    def read_config_file(self, path):
        try:
            self._config.read(path)
        except Exception as e:
            raise
        return

    def reload_config_file(self):
        try:
            self._config.read(self._path)
        except Exception as e:
            raise
        return

    def get_field(self, section, option):
        result = self._config.get(section, option)
        return result

    def get_field_list(self, section, option):
        result = self._config.get(section, option)
        return result.split(",")

    def get_section(self, section):
        result = self._config.items(section)
        return result

    def set_field(self, section, option, value):
        self._config.set(section, option, value)


GLOBAL_CONFIG = Config()
