import json

from app.api.ORM.DBDeptInfo import DBDeptInfo
from app.api.ORM.DBUserInfo import DBUserInfo
from app.api.Service.DBService import DBService


class UserInfoService(object):
    """Class FieldsInfoService"""
    def __init__(self):
        self._db_user_info_service = DBService("DBUserInfo")
        self._db_dept_info_service = DBService("DBDeptInfo")

    def find_user_info(self, attribute, content):
        obj = {"user_id": 10, "user_name": "unknown", "dept_id": 4, "role": "visitor"}
        user_info = self._db_user_info_service.db_find_one_by_attribute(attribute, content)
        if user_info is None:
            result = self.obj_2_json(obj)
        else:
            result = json.dumps(user_info, default=DBUserInfo.obj_2_json, sort_keys=False, ensure_ascii=False, indent=4)
        return result

    def find_his_dept_name(self, user_name):
        try:
            dept_id = self._db_user_info_service.db_find_one_by_attribute("user_name", user_name).dept_id
            dept_info = self._db_dept_info_service.db_find_one_by_attribute("dept_id", dept_id)
            result = json.dumps(dept_info, default=DBDeptInfo.obj_2_json_2, sort_keys=False, ensure_ascii=False, indent=4)
        except Exception as e:
            raise e
        else:
            return result

    @staticmethod
    def obj_2_json(obj):
        return json.dumps(obj, ensure_ascii=False)
