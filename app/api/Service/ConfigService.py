from Config import GLOBAL_CONFIG


class ConfigService(object):

    @staticmethod
    def check_password(admin_password):
        correct_password = GLOBAL_CONFIG.get_field("Admin","admin_password")
        if correct_password == admin_password:
            return True
        else:
            return False
