import logging
import json

from app.api.Entity.Log import Log
from app.api.Service.DBService import DBService


class LogService(object):
    """Class Log"""
    def __init__(self):
        self._db_log_service = DBService("DBLog")

    def submit_log(self, request_json):
        log_service = self.read_json(request_json)
        result = self._db_log_service.db_save(log_service)
        self._db_log_service.db_commit()
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
