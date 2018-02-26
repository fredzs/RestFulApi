"""数据库工厂"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from app.api.Factory.LogFactory import LogFactory

logger = LogFactory().get_logger()


class DBFactory(object):
    """数据库工厂"""
    def __init__(self):
        # 初始化数据库连接:
        engine = create_engine('mysql+mysqlconnector://fred_zs:some_pass@123.207.136.133:3306/ICBC', pool_recycle=50)
        # 创建DBSession类型:
        session_class = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
        # 创建session对象:
        logger.info("创建数据库连接。")
        self._db_session = session_class()

    def get_db_session(self):
        """获取数据库连接"""
        logger.info("获取数据库连接。")
        return self._db_session

    def close_session(self):
        """关闭数据库连接"""
        self._db_session.close()
        logger.info("关闭数据库连接。")
        return
