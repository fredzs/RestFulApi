"""数据库工厂"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from app.api.Factory.LogFactory import LogFactory
from Config import GLOBAL_CONFIG
logger = LogFactory().get_logger()


class DBFactory(object):
    """数据库工厂"""
    def __init__(self):
        # 初始化数据库连接:
        url = self.connect_url()
        engine = create_engine(('mysql+mysqlconnector://%s' % url), pool_recycle=50)
        # engine = create_engine('mysql+mysqlconnector://fred_zs:some_pass@123.207.136.133:3306/ICBC', pool_recycle=50)
        # 创建DBSession类型:
        session_class = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
        # 创建session对象:
        logger.debug("创建数据库连接。")
        self._db_session = session_class()

    @staticmethod
    def connect_url():
        # section = GLOBAL_CONFIG.get_section("Database")
        mode = GLOBAL_CONFIG.get_field("Setting", "mode")
        # logger.info(section)
        user_name = GLOBAL_CONFIG.get_field("Database", "user_name")
        pass_word = GLOBAL_CONFIG.get_field("Database", "pass_word")
        server_address = GLOBAL_CONFIG.get_field("Database", "server_address")
        server_port = GLOBAL_CONFIG.get_field("Database", "server_port")
        database = GLOBAL_CONFIG.get_field("Database", "database")
        if mode == "test":
            database = GLOBAL_CONFIG.get_field("Database", "test_database")

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
