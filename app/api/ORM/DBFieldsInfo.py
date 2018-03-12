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
    id = Column(Integer(), primary_key=True)
    field_id = Column(String(30))
    field_name = Column(String(30))
    business = Column(String(20))
    field_type = Column(Integer())
    field_unit = Column(String(10))
    statistics = Column(Integer())
    order_index = Column(Integer())
    status = Column(Integer())

    @staticmethod
    def obj_2_json(obj):
        return {"id": obj.id,
                "field_id": obj.field_id,
                "field_name": obj.field_name,
                #"business": obj.business,
                "field_type": obj.field_type,
                "field_unit": obj.field_unit,
                "statistics": obj.statistics,
                "order_index": obj.order_index,
                "status": True if obj.status == 1 else False}

    @staticmethod
    def obj_2_json_simple(obj):
        return {"field_id": obj.field_id, "field_name": obj.field_name, "field_type": obj.field_type, "field_unit": obj.field_unit}

