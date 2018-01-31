"""数据库工厂"""


import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DBFactory(object):
    """数据库工厂"""
    # 初始化数据库连接:
    engine = create_engine('mysql+mysqlconnector://root:fred`1234@123.207.136.133:3306/ICBC')
    # 创建DBSession类型:
    DBSession = sessionmaker(bind=engine)
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
