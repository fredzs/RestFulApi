from app.api.Entity.Config import Config


class ConfigService(object):
    def __init__(self):
        self._config = Config()
        self.read_config("config.txt")

    def read_config(self, config_file_name):
        with open(config_file_name, 'r') as f:
            for line in f:
                line = line.strip('\n')
                key = line[:line.index(' = ')]
                value = line[line.index(' = ') + 3:]
                self._config.add_config_field(key, value)

    def check_password(self, admin_password):
        correct_password = self._config.get_config_field["admin_password"]
        if correct_password == admin_password:
            return True
        else:
            return False
