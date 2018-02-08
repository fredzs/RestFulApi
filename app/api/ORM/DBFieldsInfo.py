from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()


# 定义DBDeptInfo对象:
class DBFieldsInfo(Base):
    # 表的名字:
    __tablename__ = 'fields_info'

    # 表的结构:
    field_id = Column(Integer(), primary_key=True)
    field_name = Column(String(30))
    business = Column(String(20))
    field_type = Column(Integer())
    order_index = Column(Integer())
    status = Column(Integer())

    @staticmethod
    def obj_2_json(obj):
        return {"field_name": obj.field_name,
                "business": obj.business,
                "field_type": obj.field_type,
                "order_index": obj.order_index,
                "status": obj.status}
