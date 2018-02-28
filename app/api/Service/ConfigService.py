from app import CONFIG


class ConfigService(object):

    @staticmethod
    def check_password(admin_password):
        correct_password = CONFIG.get_config_field("admin_password")
        if correct_password == admin_password:
            return True
        else:
            return False
