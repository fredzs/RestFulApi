from sqlalchemy import Column, JSON
from sqlalchemy import String
from sqlalchemy import Date
from sqlalchemy import Integer
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()


# 定义User对象:
class DBPerformance(Base):
    # 表的名字:
    __tablename__ = 'daily'

    # 表的结构:
    id = Column(Integer(), primary_key=True)
    dept_id = Column(Integer())
    date = Column(Date())
    submit_date = Column(Date())
    submit_user = Column(String(30))
    extra_fields = Column(JSON())

    @staticmethod
    def obj_2_json(obj):
        return {"submit_date": str(obj.submit_date),
                "submit_user": obj.submit_user,
                "extra_fields": obj.extra_fields}



