import logging

from sqlalchemy.exc import IntegrityError

from app.api.Factory.DBFactory import DBFactory
from app.api.ORM.DBDeptInfo import DBDeptInfo


class DBDeptInfoService(object):
    @staticmethod
    def copy_to_db(dept_info):
        db_dept_info = DBDeptInfo()
        db_dept_info.dept_type = dept_info.get_dept_type
        db_dept_info.dept_name = dept_info.get_dept_name
        db_dept_info.corporate = dept_info.get_corporate
        db_dept_info.dept_leader = dept_info.get_dept_leader
        db_dept_info.dept_vice_1 = dept_info.get_dept_vice_1
        db_dept_info.dept_vice_2 = dept_info.get_dept_vice_2
        return db_dept_info

    @staticmethod
    def db_save(dept_info):
        db_session = DBFactory.get_db_session()
        db_service = DBDeptInfoService.copy_to_db(dept_info)
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
            logging.error("提交数据库失败！")
            logging.error(e)

    @staticmethod
    def db_find_list_by_attribute(attribute, search_content):
        db_session = DBFactory().get_db_session()
        query = db_session.query(DBDeptInfo).filter(getattr(DBDeptInfo,attribute) == search_content)
        logging.debug(query)
        result = query.all()
        return result

    @staticmethod
    def db_find_column_by_attribute(attribute, search_content, column):
        db_session = DBFactory().get_db_session()
        query = db_session.query(getattr(DBDeptInfo,column)).filter(getattr(DBDeptInfo,attribute) == search_content)
        logging.debug(query)
        result = query.all()
        return result
