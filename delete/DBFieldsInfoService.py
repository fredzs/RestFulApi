import logging

from sqlalchemy.exc import IntegrityError

from app.api.Factory.DBFactory import DBFactory
from app.api.ORM.DBFieldsInfo import DBFieldsInfo


class DBFieldsInfoService(object):
    @staticmethod
    def copy_to_db(fields_info):
        db_fields_info = DBFieldsInfo()
        db_fields_info.dept_type = fields_info.field_name
        db_fields_info.dept_name = fields_info.field_type
        db_fields_info.corporate = fields_info.status
        return db_fields_info

    @staticmethod
    def db_save(dept_info):
        db_session = DBFactory.get_db_session()
        db_service = DBFieldsInfoService.copy_to_db(dept_info)
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
        query = db_session.query(DBFieldsInfoService).filter(getattr(DBFieldsInfoService,attribute) == search_content)
        logging.debug(query)
        result = query.all()
        return result

    @staticmethod
    def db_find_column_by_attribute(attribute, search_content, column):
        db_session = DBFactory().get_db_session()
        query = db_session.query(getattr(DBFieldsInfoService,column)).filter(getattr(DBFieldsInfoService,attribute) == search_content)
        logging.debug(query)
        result = query.all()
        return result

    @staticmethod
    def check_exist(date, dept_id):
        exist = None
        result = DBFieldsInfoService.db_find_column_by_attribute_list(["date", "dept_id"], [date, dept_id], "id")
        if len(result) > 0:
            exist = result[0].id
        return exist

    @staticmethod
    def db_find_column_by_attribute_list(attribute_list, search_content_list, column):
        db_session = DBFactory().get_db_session()
        query = db_session.query(getattr(DBPerformance, column))
        for attr, content in zip(attribute_list, search_content_list):
            query = query.filter(getattr(DBPerformance, attr) == content)
        logging.debug(query)
        result = query.all()
        return result
