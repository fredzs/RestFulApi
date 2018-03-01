from config import Config


class ConfigService(object):

    @staticmethod
    def check_password(admin_password):
        correct_password = Config.get_config("Admin","admin_password")
        if correct_password == admin_password:
            return True
        else:
            return False
