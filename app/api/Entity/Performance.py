"""Class Performance"""


from datetime import datetime


class Performance(object):
    """Class Performance"""
    def __init__(self, dept_id, date, submit_user='', comments="", extra_fields=None):
        self._dept_id = dept_id
        self._date = date
        self._submit_time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        self._submit_user = submit_user
        self._comments = comments
        self._extra_fields = extra_fields

    def set_dept_id(self, dept_id):
        self._dept_id = dept_id

    def set_date(self, date):
        self._date = date

    def set_submit_user(self, submit_user):
        self._submit_user = submit_user

    def set_comments(self, comments):
        self._comments = comments

    def set_extra_fields(self, extra_fields):
        self._extra_fields = extra_fields

    @property
    def get_dept_id(self):
        return self._dept_id

    @property
    def get_date(self):
        return self._date

    @property
    def get_submit_time(self):
        return self._submit_time

    @property
    def get_submit_user(self):
        return self._submit_user

    @property
    def get_comments(self):
        return self._comments

    @property
    def get_extra_fields(self):
        return self._extra_fields
