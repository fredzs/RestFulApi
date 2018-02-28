

class Config(object):
    def __init__(self):
        self._config_field = dict()

    def get_config_field(self, key):
        return self._config_field[key]

    def set_config_field(self, config_field):
        self._config_field = config_field

    def add_config_field(self, key, value):
        self._config_field[key] = value
