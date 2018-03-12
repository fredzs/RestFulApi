from sqlalchemy import Column, JSON
from sqlalchemy import String
from sqlalchemy import Date
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()


# 定义User对象:
class DBLog(Base):
    # 表的名字:
    __tablename__ = 'log'

    # 表的结构:
    log_id = Column(Integer(), primary_key=True)
    time = Column(DateTime())
    user_name = Column(String(50))
    page = Column(String(50))
    resource = Column(String(50))
    method = Column(String(50))
    content = Column(String(1000))
