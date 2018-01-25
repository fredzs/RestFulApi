import logging

from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

from Factory.DBFactory import DBFactory
from ORM.Daily import DBDaily


class DBDailyService(object):
    @staticmethod
    def copy_to_db(performance):
        db_daily = DBDaily()
        db_daily.dept_name = performance.get_dept_name
        db_daily.date = performance.get_date
        db_daily.project_1 = performance.get_project_1
        db_daily.project_2 = performance.get_project_2
        db_daily.project_3 = performance.get_project_3
        db_daily.project_4 = performance.get_project_4
        db_daily.project_5 = performance.get_project_5
        return db_daily

    @staticmethod
    def db_save(performance):
        db_session = DBFactory.get_db_session()
        db_service = DBDailyService.copy_to_db(performance)
        db_session.add(db_service)
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
            logging.error("数据库写入失败！")
            logging.error(e)

    @staticmethod
    def db_find_attribute(item_code, attribute):
        db_session = DBFactory().get_db_session()
        query = db_session.query(attribute).filter(DBDaily.item_code == item_code)
        logging.info(query)
        result = query.first()
        return result[0]

    @staticmethod
    def db_find_date_total(date):
        db_session = DBFactory().get_db_session()
        query = db_session.query(func.count('*'))
        result = query.filter(DBDaily.date == date).first()
        return result[0]
