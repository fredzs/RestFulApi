import json

from app.api.Service.DBService import DBService


class DeptInfoService(object):
    """Class FieldsInfoService"""
    def __init__(self):
        self._db_dept_info_service = DBService("DBDeptInfo")

    def find_branch_list(self, branch_name):
        branch_dept_list = self._db_dept_info_service.db_find_list_by_attribute("dept_type", 2)
        dept_name_list = dict()
        for dept in branch_dept_list:
            dept_name_list[dept.dept_id] = dept.dept_name
        result = json.dumps(dept_name_list, ensure_ascii=False)
        return result
