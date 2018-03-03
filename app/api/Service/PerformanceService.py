<<<<<<< HEAD
import logging
import json

from app.api.Entity.Performance import Performance
from app.api.Service.DBService import DBService
from app.api.Service.FieldsInfoService import FieldsInfoService


class PerformanceService(object):
    def __init__(self):
        self._db_performance_service = DBService("DBPerformance")
        self._db_dept_info_service = DBService("DBDeptInfo")
        self._db_fields_info_service = DBService("DBFieldsInfo")

    """Class Performance"""
    def submit_performance(self, request_json):
        performance = PerformanceService.read_json(request_json)
        check = self.check_exist(performance.get_date, performance.get_dept_id)
        if check is not None:
            logging.info("该条记录已存在！")
            result = self._db_performance_service.db_update(performance, check)
        else:
            result = self._db_performance_service.db_save(performance)
        if result:
            self._db_performance_service.db_commit()
            return True
        else:
            return False

    def check_exist(self, date, dept_id):
        exist = None
        result = self._db_performance_service.db_find_column_by_attribute_list(["date", "dept_id"], [date, dept_id], "id")
        if len(result) > 0:
            exist = result[0].id
        return exist

    @staticmethod
    def read_json(json_raw):
        if isinstance(json_raw, str):
            json_obj = json.loads(json_raw)
        else:
            json_obj = json_raw
        dept_id = json_obj['dept_id']
        date = json_obj['date']
        submit_user = json_obj['submit_user']
        if 'comments' in json_obj:
            comments = json_obj['comments']
        else:
            comments = ""
        extra_fields = json_obj['extra_fields']
        performance = Performance(dept_id, date, submit_user, comments, extra_fields)
        return performance

    def pre_check_submission(self, date):
        branch_dept_list = self._db_dept_info_service.db_find_list_by_attribute("dept_type", 2)
        performance_list = self._db_performance_service.db_find_list_by_attribute("date", date)
        done_list, submission_list, unsubmission_list = [], [], []
        dept_name_list = dict()

        for dept in branch_dept_list:
            dept_name_list[dept.dept_id] = dept.dept_name
        for performance in performance_list:
            done_list.append({"dept_id": performance.dept_id, "submit_user": performance.submit_user})
        for item in dept_name_list:
            c = False
            for i, p in enumerate(performance_list):
                if item == p.dept_id:
                    submission_list.append({"dept_name": dept_name_list[p.dept_id], "submit_user": p.submit_user})
                    c = True
                    break
            if not c:
                unsubmission_list.append({"dept_name": dept_name_list[item]})

        return submission_list, unsubmission_list

    def check_submission(self, date):
        submission_list, unsubmission_list = self.pre_check_submission(date)
        json_data = {"date": date.strftime("%Y-%m-%d"), "submission_list": submission_list,
                     "unsubmission_list": unsubmission_list}
        result = self.obj_2_json(json_data)
        return result

    @staticmethod
    def obj_2_json(obj):
        return json.dumps(obj, ensure_ascii=False)

    def display(self, date, dept_name):
        performance = {}
        obj = self.find_performance_by_date(date, "dept_name", dept_name)
        if len(obj) > 0:
            d = obj[0]
            performance = {"submit_user": d.submit_user,
                           "date": str(d.date),
                           "submit_time": str(d.submit_time),
                           "comments": d.comments,
                           "extra_fields": self.rewrite_extra_fields(d.extra_fields)}
        result = self.obj_2_json(performance)
        return result

    def find(self, date, dept_id):
        performance = {"submit_user": "", "submit_time": ""}
        obj = self.find_performance_by_date(date, "dept_id",  dept_id)
        if len(obj) > 0:
            d = obj[0]
            performance = {"submit_user": d.submit_user, "submit_time": str(d.submit_time)}
        result = self.obj_2_json(performance)
        return result

    def find_performance_by_date(self, date, attribute, content):
        dept_id = self._db_dept_info_service.db_find_column_by_attribute(attribute, content, "dept_id")[0].dept_id
        db = self._db_performance_service.db_find_list_by_attribute_list(["date", "dept_id"], [date, dept_id])
        return db

    def rewrite_extra_fields(self, extra_fields):
        extra_fields_full = []
        fields_list = self._db_fields_info_service.db_find_list_by_attribute_list_order_by(["business", "status"],
                                                                                           ["corporate", "1"],
                                                                                           "order_index")
        name_list = {}
        unit_list = {}
        status_list = []
        for item in fields_list:
            name_list[item.field_id] = item.field_name
            unit_list[item.field_id] = item.field_unit
            status_list.append(item.field_id)
        for field in extra_fields:
            if field in status_list:
                extra_fields_full.append({"field_name": name_list[field], "field_value": extra_fields[field], "field_unit": unit_list[field]})
        return extra_fields_full
=======
import logging
import json

from app.api.Entity.Performance import Performance
from app.api.Service.DBService import DBService
from app.api.Service.FieldsInfoService import FieldsInfoService


class PerformanceService(object):
    def __init__(self):
        self._db_performance_service = DBService("DBPerformance")
        self._db_dept_info_service = DBService("DBDeptInfo")
        self._db_fields_info_service = DBService("DBFieldsInfo")

    """Class Performance"""
    def submit_performance(self, request_json):
        performance = PerformanceService.read_json(request_json)
        check = self.check_exist(performance.get_date, performance.get_dept_id)
        if check is not None:
            logging.info("该条记录已存在！")
            result = self._db_performance_service.db_update(performance, check)
        else:
            result = self._db_performance_service.db_save(performance)
        if result:
            self._db_performance_service.db_commit()
            return True
        else:
            return False

    def check_exist(self, date, dept_id):
        exist = None
        result = self._db_performance_service.db_find_column_by_attribute_list(["date", "dept_id"], [date, dept_id], "id")
        if len(result) > 0:
            exist = result[0].id
        return exist

    @staticmethod
    def read_json(json_raw):
        if isinstance(json_raw, str):
            json_obj = json.loads(json_raw)
        else:
            json_obj = json_raw
        dept_id = json_obj['dept_id']
        date = json_obj['date']
        submit_user = json_obj['submit_user']
        if 'comments' in json_obj:
            comments = json_obj['comments']
        else:
            comments = ""
        extra_fields = json_obj['extra_fields']
        performance = Performance(dept_id, date, submit_user, comments, extra_fields)
        return performance

    def pre_check_submission(self, date):
        branch_dept_list = self._db_dept_info_service.db_find_list_by_attribute("dept_type", 2)
        performance_list = self._db_performance_service.db_find_list_by_attribute("date", date)
        done_list, submission_list, unsubmission_list = [], [], []
        dept_name_list = dict()

        for dept in branch_dept_list:
            dept_name_list[dept.dept_id] = dept.dept_name
        for performance in performance_list:
            done_list.append({"dept_id": performance.dept_id, "submit_user": performance.submit_user})
        for item in dept_name_list:
            c = False
            for i, p in enumerate(performance_list):
                if item == p.dept_id:
                    submission_list.append({"dept_name": dept_name_list[p.dept_id], "submit_user": p.submit_user})
                    c = True
                    break
            if not c:
                unsubmission_list.append({"dept_name": dept_name_list[item]})

        return submission_list, unsubmission_list

    def check_submission(self, date):
        submission_list, unsubmission_list = self.pre_check_submission(date)
        json_data = {"date": date.strftime("%Y-%m-%d"), "submission_list": submission_list,
                     "unsubmission_list": unsubmission_list}
        result = self.obj_2_json(json_data)
        return result

    @staticmethod
    def obj_2_json(obj):
        return json.dumps(obj, ensure_ascii=False)

    def display(self, date, dept_name):
        performance = {}
        obj = self.find_performance_by_date(date, "dept_name", dept_name)
        if len(obj) > 0:
            d = obj[0]
            performance = {"submit_user": d.submit_user,
                           "date": str(d.date),
                           "submit_time": str(d.submit_time),
                           "comments": d.comments,
                           "extra_fields": self.rewrite_extra_fields(d.extra_fields)}
        result = self.obj_2_json(performance)
        return result

    def find(self, date, dept_id):
        performance = {"submit_user": "", "submit_time": ""}
        obj = self.find_performance_by_date(date, "dept_id",  dept_id)
        if len(obj) > 0:
            d = obj[0]
            performance = {"submit_user": d.submit_user, "submit_time": str(d.submit_time)}
        result = self.obj_2_json(performance)
        return result

    def find_performance_by_date(self, date, attribute, content):
        dept_id = self._db_dept_info_service.db_find_column_by_attribute(attribute, content, "dept_id")[0].dept_id
        db = self._db_performance_service.db_find_list_by_attribute_list(["date", "dept_id"], [date, dept_id])
        return db

    def find_performance_by_range(self, date_begin, data_end, attribute, content):
        dept_id = self._db_dept_info_service.db_find_column_by_attribute(attribute, content, "dept_id")[0].dept_id
        db = self._db_performance_service.db_find_list_by_attribute_list2(["date", "dept_id"], [[date_begin, data_end], dept_id])
        return db

    def rewrite_extra_fields(self, extra_fields):
        extra_fields_full = []
        fields_list = self._db_fields_info_service.db_find_list_by_attribute_list_order_by(["business", "status"],
                                                                                           ["corporate", "1"],
                                                                                           "order_index")
        name_list = {}
        unit_list = {}
        order_list = []
        for item in fields_list:
            name_list[item.field_id] = item.field_name
            unit_list[item.field_id] = item.field_unit
            order_list.append(item.field_id)
        for field_id in order_list:
            if field_id in extra_fields:
                extra_fields_full.append({"field_name": name_list[field_id], "field_value": extra_fields[field_id], "field_unit": unit_list[field_id]})
        return extra_fields_full
>>>>>>> b010fb2eff0d466ec73f41c8703ee1e64d6543ac
