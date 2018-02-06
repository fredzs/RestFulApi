from sqlalchemy import Column, JSON
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
    submit_user = Column(String(30))
    project_1 = Column(Integer())
    extra_fields = Column(JSON())







