from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()


# 定义DBUserInfo对象:
class DBUserInfo(Base):
    # 表的名字:
    __tablename__ = 'user_info'

    # 表的结构:
    user_id = Column(Integer(), primary_key=True)
    user_name = Column(String(20))
    wx_nick_name = Column(String(30))
    dept_id = Column(Integer())
    role = Column(Integer())

    @staticmethod
    def obj_2_json(obj):
        return {"user_id": obj.user_id,
                "user_name": obj.user_name,
                "dept_id": obj.dept_id,
                "role": obj.role}
