'''Class Performance'''


class Performance(object):
    '''Class Performance'''
    def __init__(self, dept_name, date, submit_user='', project1=0, extra_fields=None):
        if extra_fields is None:
            extra_fields = {"field_1": ""}
        self._dept_name = dept_name
        self._date = date
        self._submit_user = submit_user
        self._project_1 = project1
        self._extra_fields = extra_fields

    def set_dept_name(self, dept_name):
        self._dept_name = dept_name

    def set_date(self, date):
        self._date = date

    def set_submit_user(self, submit_user):
        self._submit_user = submit_user

    def set_project_1(self, project_1):
        self._project_1 = project_1

    def set_extra_fields(self, extra_fields):
        self._extra_fields = extra_fields

    @property
    def get_dept_name(self):
        return self._dept_name

    @property
    def get_date(self):
        return self._date

    @property
    def get_submit_user(self):
        return self._submit_user

    @property
    def get_project_1(self):
        return self._project_1

    @property
    def get_extra_fields(self):
        return self._extra_fields
