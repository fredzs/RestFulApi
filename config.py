import os
import configparser
# from app.api.Factory.LogFactory import LogFactory
# logging = LogFactory().get_logger()


class Config(object):

    @staticmethod
    def get_config(section, key):
        cfg = configparser.ConfigParser()
        path = os.path.join(os.path.split(os.path.realpath(__file__))[0] + '/config.ini')
        # logging.error("在路径%s寻找配置文件。。。" % path)
        try:
            cfg.read(path)
            result = cfg.get(section, key)
        except Exception as e:
            # logging.error("读取配置文件错误！")
            raise
        # logging.error("读取配置文件:%s" % result)
        return result

    @staticmethod
    def get_section(section):
        cfg = configparser.ConfigParser()
        path = os.path.join(os.path.split(os.path.realpath(__file__))[0] + '/config.ini')
        # logging.error("在路径%s寻找配置文件。。。" % path)
        try:
            cfg.read(path)
            result = cfg.items(section)
        except Exception as e:
            # logging.error("读取配置文件错误！")
            raise
        # logging.error("读取配置文件:%s" % result)
        return result
