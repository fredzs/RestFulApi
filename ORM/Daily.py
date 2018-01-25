from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Date
from sqlalchemy import Integer
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()


# 定义User对象:
class DBDaily(Base):
    # 表的名字:
    __tablename__ = 'daily'

    # 表的结构:
    id = Column(Integer(), primary_key=True)
    dept_name = Column(String(20))
    date = Column(Date())
    project_1 = Column(Integer())
    project_2 = Column(String(20))
    project_3 = Column(String(20))
    project_4 = Column(String(20))
    project_5 = Column(String(20))







