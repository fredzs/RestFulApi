import logging
import json

from app.api.Entity.Log import Log
from app.api.Service.DBService import DBService


class LogService(object):
    """Class Log"""
    db_log_service = DBService("DBLog")

    @staticmethod
    def submit_log_json(request_json):
        log = LogService.read_json(request_json)
        result = LogService.db_log_service.db_save(log)
        LogService.db_log_service.db_commit()
        return result

    @staticmethod
    def submit_log(user_name, page, method, content):
        if isinstance(content, str):
            content_obj = json.loads(content)
        else:
            content_obj = str(content)
        log = Log(user_name, page, method, content_obj)
        result = LogService.db_log_service.db_save(log)
        LogService.db_log_service.db_commit()
        return result

    @staticmethod
    def read_json(json_raw):
        if isinstance(json_raw, str):
            json_obj = json.loads(json_raw)
        else:
            json_obj = json_raw
        user_name = json_obj['user_name']
        page = json_obj['page']
        method = json_obj['method']
        content = json_obj['content']
        log = Log(user_name, page, method, content)
        return log
