from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()


# 定义DBDeptInfo对象:
class DBDeptInfo(Base):
    # 表的名字:
    __tablename__ = 'dept_info'

    # 表的结构:
    dept_id = Column(Integer(), primary_key=True)
    dept_type = Column(Integer())
    dept_name = Column(String(50))
    corporate = Column(Integer())
    dept_leader = Column(String(10))
    dept_vice_1 = Column(String(20))
    dept_vice_2 = Column(String(20))

    @staticmethod
    def obj_2_json(obj):
        return {"dept_id": obj.dept_id,
                "dept_name": obj.dept_name}

    @staticmethod
    def obj_2_json_2(obj):
        return {"dept_id": obj.dept_id,
                "dept_name": obj.dept_name,
                "dept_type": obj.dept_type}



