import logging
import json

from app.api.Entity.Performance import Performance
from app.api.Service.DBService import DBService


class PerformanceService(object):
    def __init__(self):
        self._db_performance_service = DBService("DBPerformance")
        self._db_dept_info_service = DBService("DBDeptInfo")

    """Class Performance"""
    def submit_performance(self, performance):
        check = self._db_performance_service.check_exist(performance.get_date, performance.get_dept_id)
        if check is not None:
            logging.info("该条记录已存在！")
            self._db_performance_service.db_update(performance, check)
        else:
            self._db_performance_service.db_save(performance)
        self._db_performance_service.db_commit()

    @staticmethod
    def read_json(json_raw):
        if isinstance(json_raw, str):
            json_obj = json.loads(json_raw)
        else:
            json_obj = json_raw
        dept_id = json_obj['dept_id']
        date = json_obj['date']
        submit_user = json_obj['submit_user']
        extra_fields = json_obj['extra_fields']
        performance = Performance(dept_id, date, submit_user, extra_fields)
        return performance

    def check_submission(self, date):
        branch_dept_list = self._db_dept_info_service.db_find_list_by_attribute("dept_type", 2)
        performance_list = self._db_performance_service.db_find_column_by_attribute("date", date, "dept_id")
        done_list, submission_list, unsubmission_list =[], [], []
        dept_name_list = dict()

        for dept in branch_dept_list:
            dept_name_list[dept.dept_id] = dept.dept_name
        for performance in performance_list:
            done_list.append(performance.dept_id)
        for item in dept_name_list:
            if item in done_list:
                submission_list.append(dept_name_list[item])
            else:
                unsubmission_list.append(dept_name_list[item])
        json_data = {"date": date.strftime("%Y-%m-%d"), "submission_list": submission_list, "unsubmission_list": unsubmission_list}
        result = json.dumps(json_data, ensure_ascii=False)
        # logging.info("%s已提交业绩的网点有：%s" % (date.strftime('%Y-%m-%d'), submission_list))
        # logging.info("%s尚未提交业绩的网点有：%s" % (date.strftime('%Y-%m-%d'), unsubmission_list))
        return result
