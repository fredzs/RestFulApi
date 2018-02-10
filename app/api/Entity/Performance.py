"""Class Performance"""


from datetime import datetime


class Performance(object):
    """Class Performance"""
    def __init__(self, dept_id, date, submit_user='', extra_fields=None):
        self._dept_id = dept_id
        self._date = date
        self._submit_date = datetime.today().strftime('%Y-%m-%d')
        self._submit_user = submit_user
        self._extra_fields = extra_fields

    @staticmethod
    def rewrite_extra_fields(extra_fields):
        extra_fields_full = []
        for field in extra_fields:
            extra_fields_full.append({"field_id": field, "field_value": extra_fields[field]})
            # {"field_1": "300", "field_2": "100", "field_3": "15"}
            # [{"field_id": "field_1", "field_value": 300}, {"field_id": "field_2", "field_value": 100}, {"field_id": "field_3", "field_value": 15}]
        return extra_fields_full

    def set_dept_id(self, dept_id):
        self._dept_id = dept_id

    def set_date(self, date):
        self._date = date

    def set_submit_user(self, submit_user):
        self._submit_user = submit_user

    def set_extra_fields(self, extra_fields):
        self._extra_fields = extra_fields

    @property
    def get_dept_id(self):
        return self._dept_id

    @property
    def get_date(self):
        return self._date

    @property
    def get_submit_date(self):
        return self._submit_date

    @property
    def get_submit_user(self):
        return self._submit_user

    @property
    def get_extra_fields(self):
        return self._extra_fields
