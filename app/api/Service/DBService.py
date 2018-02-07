import logging

import sys

from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

from app.api.Factory.DBFactory import DBFactory
from app.api.ORM.DBPerformance import DBPerformance
from app.api.ORM.DBDeptInfo import DBDeptInfo
from app.api.ORM.DBFieldsInfo import DBFieldsInfo


class DBService(object):
    def __init__(self, class_name):
        self._db_class = eval(class_name)
        self._db_factory = DBFactory()
        self._db_session = self._db_factory.get_db_session()

    def __del__(self):
        pass
        # self._db_factory.close_session()

    def copy_to_db(self, performance, update_id=None):
        db_performance = self._db_class
        if update_id is not None:
            db_performance.id = update_id
        db_performance.dept_id = performance.get_dept_id
        db_performance.date = performance.get_date
        db_performance.submit_date = performance.get_submit_date
        db_performance.submit_user = performance.get_submit_user
        db_performance.extra_fields = performance.get_extra_fields
        return db_performance

    def db_save(self, performance):
        self._db_session = DBFactory.get_db_session()
        db_service = self.copy_to_db(performance)
        self._db_session.add(db_service)
        logging.info("已写入数据库缓存")
        return

    def db_update(self, performance, update_id):
        self._db_session = DBFactory.get_db_session()
        db_service = self.copy_to_db(performance, update_id)
        self._db_session.merge(db_service)
        logging.info("已写入数据库缓存")
        return

    def db_commit(self):
        self._db_session = DBFactory.get_db_session()
        try:
            self._db_session.flush()
            self._db_session.commit()
            logging.info("已提交数据库")
        except IntegrityError as e:
            self._db_session.rollback()
            logging.error("记录重复")
            logging.error(e)
        except Exception as e:
            logging.error("提交数据库失败！")
            logging.error(e)

    def db_find_list_by_attribute(self, attribute, search_content):
        self._db_session = DBFactory().get_db_session()
        query = self._db_session.query(self._db_class).filter(getattr(self._db_class, attribute) == search_content)
        logging.debug(query)
        result = query.all()
        return result

    def db_find_list_by_attribute_order_by(self, attribute, search_content, order_by):
        self._db_session = DBFactory().get_db_session()
        query = self._db_session.query(self._db_class).order_by(getattr(self._db_class, order_by).asc()).filter(getattr(self._db_class, attribute) == search_content)
        logging.debug(query)
        result = query.all()
        return result

    def db_find_date_total(self, date):
        self._db_session = DBFactory().get_db_session()
        query = self._db_session.query(func.count('*'))
        result = query.filter(self._db_class.submit_date == date).first()
        return result[0]

    def db_find_column_by_attribute(self, attribute, search_content, column):
        self._db_session = DBFactory().get_db_session()
        query = self._db_session.query(getattr(self._db_class, column)).filter(
            getattr(self._db_class, attribute) == search_content)
        logging.debug(query)
        result = query.all()
        return result

    def db_find_column_by_attribute_list(self, attribute_list, search_content_list, column):
        self._db_session = DBFactory().get_db_session()
        query = self._db_session.query(getattr(self._db_class, column))
        for attr, content in zip(attribute_list, search_content_list):
            query = query.filter(getattr(self._db_class, attr) == content)
        logging.debug(query)
        result = query.all()
        return result

    def check_exist(self, date, dept_id):
        exist = None
        result = self.db_find_column_by_attribute_list(["date", "dept_id"], [date, dept_id], "id")
        if len(result) > 0:
            exist = result[0].id
        return exist
