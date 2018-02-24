"""数据库工厂"""


import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


class DBFactory(object):
    """数据库工厂"""
    # 初始化数据库连接:
    engine = create_engine('mysql+mysqlconnector://fred_zs:some_pass@123.207.136.133:3306/ICBC', pool_recycle=3600)
    # 创建DBSession类型:
    #DBSession = sessionmaker(bind=engine)
    DBSession = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    # 创建session对象:
    db_session = DBSession()

    @staticmethod
    def get_db_session():
        """获取数据库连接"""
        return DBFactory.db_session

    @staticmethod
    def close_session():
        """关闭数据库连接"""
        DBFactory.db_session.close()
        logging.info("关闭数据库连接。")
