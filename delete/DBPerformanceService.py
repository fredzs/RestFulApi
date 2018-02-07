import logging

from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

from app.api.Factory.DBFactory import DBFactory
from app.api.ORM.DBPerformance import DBPerformance


class DBPerformanceService(object):
    @staticmethod
    def copy_to_db(performance, update_id=None):
        db_performance = DBPerformance()
        if update_id is not None:
            db_performance.id = update_id
        db_performance.dept_id = performance.get_dept_id
        db_performance.date = performance.get_date
        db_performance.submit_date = performance.get_submit_date
        db_performance.submit_user = performance.get_submit_user
        db_performance.extra_fields = performance.get_extra_fields
        return db_performance

    @staticmethod
    def db_save(performance):
        db_session = DBFactory.get_db_session()
        db_service = DBPerformanceService.copy_to_db(performance)
        db_session.add(db_service)
        logging.info("已写入数据库缓存")
        return

    @staticmethod
    def db_update(performance, update_id):
        db_session = DBFactory.get_db_session()
        db_service = DBPerformanceService.copy_to_db(performance, update_id)
        db_session.merge(db_service)
        logging.info("已写入数据库缓存")
        return

    @staticmethod
    def db_commit():
        db_session = DBFactory.get_db_session()
        try:
            db_session.flush()
            db_session.commit()
            logging.info("已提交数据库")
        except IntegrityError as e:
            db_session.rollback()
            logging.error("记录重复")
            logging.error(e)
        except Exception as e:
            logging.error("提交数据库失败！")
            logging.error(e)

    @staticmethod
    def db_find_list_by_attribute(attribute, search_content):
        db_session = DBFactory().get_db_session()
        query = db_session.query(DBPerformance).filter(getattr(DBPerformance, attribute) == search_content)
        logging.debug(query)
        result = query.first()
        return result

    @staticmethod
    def db_find_date_total(date):
        db_session = DBFactory().get_db_session()
        query = db_session.query(func.count('*'))
        result = query.filter(DBPerformance.submit_date == date).first()
        return result[0]

    @staticmethod
    def db_find_column_by_attribute(attribute, search_content, column):
        db_session = DBFactory().get_db_session()
        query = db_session.query(getattr(DBPerformance, column)).filter(getattr(DBPerformance, attribute) == search_content)
        logging.debug(query)
        result = query.all()
        return result

    @staticmethod
    def db_find_column_by_attribute_list(attribute_list, search_content_list, column):
        db_session = DBFactory().get_db_session()
        query = db_session.query(getattr(DBPerformance, column))
        for attr, content in zip(attribute_list, search_content_list):
            query = query.filter(getattr(DBPerformance, attr) == content)
        logging.debug(query)
        result = query.all()
        return result

    @staticmethod
    def check_exist(date, dept_id):
        exist = None
        result = DBPerformanceService.db_find_column_by_attribute_list(["date", "dept_id"], [date, dept_id], "id")
        if len(result) > 0:
            exist = result[0].id
        return exist
