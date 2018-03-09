import sys

from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

from app.api.Factory.DBFactory import DBFactory
from app.api.ORM.DBPerformance import DBPerformance
from app.api.ORM.DBDeptInfo import DBDeptInfo
from app.api.ORM.DBFieldsInfo import DBFieldsInfo
from app.api.ORM.DBUserInfo import DBUserInfo
from app.api.ORM.DBLog import DBLog
from app.api.Factory.LogFactory import LogFactory

logger = LogFactory().get_logger()


class DBService(object):
    def __init__(self, class_type):
        self._db_class = eval(class_type)
        self._db_instance = eval(class_type + "()")
        self._db_factory = DBFactory()
        self._db_session = self._db_factory.get_db_session()

    def __del__(self):
        self._db_factory.close_session()

    def copy_to_db(self, instance, update_id=None):
        db_obj = self._db_instance
        if update_id is not None:
            db_obj.id = update_id
        for attr in instance.__dict__:
            attr_1 = attr[1:]
            setattr(db_obj, attr_1, getattr(instance, attr))
        return db_obj

    def db_save(self, performance):
        db_service = self.copy_to_db(performance)
        try:
            self._db_session.add(db_service)
        except Exception as e:
            logger.info("写入数据库缓存失败:%s" % e)
            raise Exception
        logger.info("已写入数据库缓存")
        return True

    def db_update(self, field, update_id):
        db_service = self.copy_to_db(field, update_id)
        try:
            self._db_session.merge(db_service)
        except Exception as e:
            logger.info("写入数据库缓存失败:%s" % e)
            return False
        logger.info("已写入数据库缓存")
        return True

    def db_update_db(self, db_obj):
        try:
            self._db_session.merge(db_obj)
        except Exception as e:
            logger.info("写入数据库缓存失败:%s" % e)
            return False
        logger.info("已写入数据库缓存")
        self.db_commit()
        return True

    def db_commit(self):
        try:
            self._db_session.flush()
            self._db_session.commit()
            logger.info("已提交数据库")
        except IntegrityError as e:
            self._db_session.rollback()
            logger.error("记录重复")
            logger.error(e)
        except Exception as e:
            logger.error("提交数据库失败！")
            logger.error(e)

    def db_find_list_by_attribute(self, attribute, search_content):
        query = self._db_session.query(self._db_class).filter(getattr(self._db_class, attribute) == search_content)
        logger.debug(query)
        result = query.all()
        return result

    def db_find_list_by_attribute_order_by(self, attribute, search_content, order_by):
        query = self._db_session.query(self._db_class).order_by(getattr(self._db_class, order_by).asc()).filter(getattr(self._db_class, attribute) == search_content)
        logger.debug(query)
        result = query.all()
        return result

    def db_find_list_by_attribute_list_order_by(self, attribute_list, search_content_list, order_by):
        query = self._db_session.query(self._db_class).order_by(getattr(self._db_class, order_by).asc())
        for attr, content in zip(attribute_list, search_content_list):
            query = query.filter(getattr(self._db_class, attr) == content)
        logger.debug(query)
        result = query.all()
        return result

    def db_find_list_by_attribute_list(self, attribute_list, search_content_list):
        query = self._db_session.query(self._db_class)
        for attr, content in zip(attribute_list, search_content_list):
            query = query.filter(getattr(self._db_class, attr) == content)
        logger.debug(query)
        result = query.all()
        return result

    def db_find_list_by_attribute_list2(self, attribute_list, search_content_list):
        query = self._db_session.query(self._db_class)
        for attr, content in zip(attribute_list, search_content_list):
            if isinstance(content, list):
                if len(content) == 2:
                    query = query.filter(getattr(self._db_class, attr) <= content[1]).filter(content[0] <= getattr(self._db_class, attr))
            else:
                query = query.filter(getattr(self._db_class, attr) == content)
        logger.debug(query)
        result = query.all()
        return result

    def db_find_column_by_attribute(self, attribute, search_content, column):
        query = self._db_session.query(getattr(self._db_class, column)).filter(
            getattr(self._db_class, attribute) == search_content)
        logger.debug(query)
        result = query.all()
        return result

    def db_find_one_by_attribute(self, attribute, search_content):
        query = self._db_session.query(self._db_class).filter(
            getattr(self._db_class, attribute) == search_content)
        logger.debug(query)
        result = query.first()
        return result

    def db_find_column_by_attribute_list(self, attribute_list, search_content_list, column):
        query = self._db_session.query(getattr(self._db_class, column))
        for attr, content in zip(attribute_list, search_content_list):
            query = query.filter(getattr(self._db_class, attr) == content)
        logger.debug(query)
        result = query.all()
        return result

    def db_find_date_total(self, date):
        query = self._db_session.query(func.count('*'))
        result = query.filter(self._db_class.submit_date == date).first()
        return result[0]

    def db_find_max_id(self):
        query = self._db_session.query(self._db_class).order_by(getattr(self._db_class, "id").desc())
        result = query.first()
        return result

    def db_find_max_order(self):
        query = self._db_session.query(self._db_class).order_by(getattr(self._db_class, "order_index").desc())
        result = query.first()
        return result

    def db_find_by_attribute_list_from_multi_table(self, attribute_list, search_content_list, query_str, class_type_2):
        db_class_join = eval(class_type_2)
        query = self._db_session.query(query_str)
        for attr, content in zip(attribute_list, search_content_list):
            query = query.filter(getattr(self._db_class, attr) == content)
        logger.debug(query)
        result = query.all()
        return result
