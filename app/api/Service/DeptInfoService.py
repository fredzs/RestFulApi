import json

from app.api.ORM.DBDeptInfo import DBDeptInfo
from app.api.Service.DBService import DBService


class DeptInfoService(object):
    """Class FieldsInfoService"""
    def __init__(self):
        self._db_dept_info_service = DBService("DBDeptInfo")

    def find_branch_list(self, branch_name):
        branch_dept_list = self._db_dept_info_service.db_find_list_by_attribute("dept_type", 2)
        result = json.dumps(branch_dept_list, default=DBDeptInfo.obj_2_json, sort_keys=False, ensure_ascii=False, indent=4)
        return result

    def find_branch_kv_list(self, branch_name):
        branch_dept_list = self._db_dept_info_service.db_find_list_by_attribute("dept_type", 2)
        result = []
        for branch in branch_dept_list:
            result.append({"dept_name": branch.dept_name})
        return result
