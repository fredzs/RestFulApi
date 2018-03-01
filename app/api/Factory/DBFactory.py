"""数据库工厂"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from app.api.Factory.LogFactory import LogFactory
from config import Config
logger = LogFactory().get_logger()


class DBFactory(object):
    """数据库工厂"""
    def __init__(self):
        # 初始化数据库连接:
        # url = self.connect_url()
        # engine = create_engine(('mysql+mysqlconnector://%s' % url), pool_recycle=50)
        engine = create_engine('mysql+mysqlconnector://fred_zs:some_pass@123.207.136.133:3306/ICBC', pool_recycle=50)
        # 创建DBSession类型:
        session_class = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
        # 创建session对象:
        logger.debug("创建数据库连接。")
        self._db_session = session_class()

    @staticmethod
    def connect_url():
        # section = Config.get_section("Database")
        # logger.info(section)
        # user_name = section["user_name"]
        # pass_word = section["pass_word"]
        # server_address = section["server_address"]
        # server_port = section["server_port"]
        # database = section["database"]
        user_name = Config.get_config("Database","user_name")
        pass_word = Config.get_config("Database","pass_word")
        server_address = Config.get_config("Database","server_address")
        server_port = Config.get_config("Database","server_port")
        database = Config.get_config("Database","database")
        url = "%s:%s@%s:%s/%s" % (user_name, pass_word, server_address, server_port, database)
        return url

    def get_db_session(self):
        """获取数据库连接"""
        logger.debug("获取数据库连接。")
        return self._db_session

    def close_session(self):
        """关闭数据库连接"""
        self._db_session.close()
        logger.debug("关闭数据库连接。")
        return
